import time
from src.arquivo import search_arquivo
from src.utils import *
from src.dbmongo import DbMongo, get_db
from src.cdx import *
from loguru import logger
from newspaper import Article
from concurrent.futures import ThreadPoolExecutor
import spacy
from collections import defaultdict

nlp = spacy.load("pt_core_news_sm")
SLEEP_BETWEEN_LOOPS = 5
LIMIT_FETCH = 500


@logger.catch
def extract_entities(db, n):
    logger.info("parsing entities %s" % n["title"])
    text = "%s\n%s" % (n["title"], n["text"])
    doc = nlp(text)
    entities = []
    seen = set()
    for ent in list(doc.ents) + ner_exceptions(text):
        if len(ent.text) <= 1: continue
        ent_id = name_to_id(ent.text)
        # entities collection
        if ent.text not in seen:
            entities.append({"_id": ent_id, "text": ent.text, "label": ent.label_, "news": [n["_id"]]})
        seen.add(ent.text)
        # news collection
        n["entities"][ent.label_].append((ent_id, ent.text))
    for label in n["entities"]:
        n["entities"][label] = set_from_tuples_list(n["entities"][label])
    n["processed_entities"] = True
    db.upsert_news_piece(n)
    db.upsert_entities(entities)


@logger.catch
def explore_entities(config):
    # iterate all unexplored news and get its entities
    db = get_db(config)
    while True:  # db.has_unexplored_news_entities():
        logger.warning("New explore entities loop")
        # for n in db.get_unexplored_news_entities().limit(LIMIT_FETCH):
        #     extract_entities(db, n)
        with ThreadPoolExecutor() as pool:
            pool.map(
                lambda n: extract_entities(db, n),
                db.get_unexplored_news_entities().limit(500)
            )
        time.sleep(SLEEP_BETWEEN_LOOPS)  # sleep waiting for other threads to do their part


@logger.catch
def explore_news_piece(db, n):
    logger.info("fetching %s" % n["url"])
    a = Article(n["url"], _language="pt")
    html = try_request(n["url"])
    if not html:
        if html == False:  # resource will never be available
            n["valid"] = False
            n["processed"] = True
            logger.error("%s will never be available" % (n["url"]))
            db.upsert_news_piece(n)
        return
    a.download(input_html=html.text)
    try:
        a.parse()
        text = assert_valid_article(a)
        # logger.info("%s[%s]" % (n["_id"], n["url"]))
        n["text"] = text
        n["image"] = a.top_image
    except Exception as e:
        logger.error("[%s] while parsing %s" % (e, n))
        n["valid"] = False
    n["processed"] = True
    db.upsert_news_piece(n)
    logger.info("done %s" % n["url"])


@logger.catch
def explore_news(config):
    # iterate all unexpanded news articles in the database
    db = get_db(config)
    while True:  # db.has_unexplored_news():
        logger.warning("New explore news loop")
        with ThreadPoolExecutor() as pool:
            # for n in db.get_unexplored_news().limit(LIMIT_FETCH):
            #     explore_news_piece(db, n)
            pool.map(
                lambda n: explore_news_piece(db, n),
                db.get_unexplored_news().limit(LIMIT_FETCH)
            )
        time.sleep(SLEEP_BETWEEN_LOOPS)  # sleep waiting for other threads to do their part


@logger.catch
def explore_person(config, db, person, site, intervals):
    logger.info("Exploring news for %s in %s" % (person["_id"], site))
    for _from, _to in intervals:
        if not valid_website(site, _from, _to): continue
        # perform search
        news = search_arquivo(person["name"], _from, _to, [site], max_items=config["max_news_batch"])
        clean_news = []
        for n in news:
            try:
                cn = DbMongo._clean_news_piece(n, (person["_id"], person["name"]))
                if cn: clean_news.append(cn)
            except Exception as e:
                logger.error("ERROR: %s in clean_news: %s" % (e, n))
        logger.info("Got %d clean news for %s (%s, %s) in %s" % (len(clean_news), person["_id"], _from, _to, site))
        # print(Counter([n["website"] for n in news]))
        db.upsert_news(clean_news)


@logger.catch
def explore_people(config):
    # iterate all people and search arquivo.pt for them
    db = get_db(config)
    intervals = split_between_dates(config["from"], config["to"])
    while True:  # db.has_unexplored_people():
        logger.warning("New explore people loop")
        try:
            for person in db.get_unexplored_people().limit(LIMIT_FETCH):
                # for site in config["websites"]:
                #     explore_person(config, db, person, site, intervals)
                with ThreadPoolExecutor() as pool:
                    pool.map(
                        lambda site: explore_person(config, db, person, site, intervals),
                        config["websites"]
                    )
                person["processed"] = True
                db.upsert_person(person)
        except Exception as e:
            logger.error("A rare exception [%s] on explore_people" % e)
        time.sleep(SLEEP_BETWEEN_LOOPS) # sleep waiting for other threads to do their part


@logger.catch
def extract_next_round_people(config, db):
    logger.warning("Extracting next round of people")
    db.update_entity_len()
    ignore_people = list(set(config["ignore_people"] + config["actually_orgs"]))
    logger.info("Ignoring: %s" % ignore_people)
    db.delete_ignored_people(ignore_people)
    explored = db.get_explored_people_ids()
    logger.info("explored: %s" % explored)
    logger.info("updating duplicate entries")
    db.update_duplicate_entities()
    logger.info("updating 'actually_orgs'")
    db.update_entities_to(config["actually_orgs"], "ORG")
    logger.info("select most_mentioned")
    potential = db.get_most_mentioned(ignore_people + explored, min_len=config["min_occurrences_before_inserted"], limit=config["max_new_users_per_round"])
    new_people = [{"_id": p["_id"], "name": p["text"]} for p in potential]
    logger.info(str(list(new_people)))
    db.upsert_people(new_people)


@logger.catch
def next_round(config):
    db = get_db(config)
    rounds = 0
    while rounds < config["rounds"]:
        while db.has_unexplored_people() or db.has_unexplored_news() or db.has_unexplored_news_entities():
            time.sleep(10)
        # all threads completed: check if there are still things to process:
        logger.success("db.has_unexplored_people(): %s" % db.has_unexplored_people())
        logger.success("db.has_unexplored_news(): %s" % db.has_unexplored_news())
        logger.success("db.has_unexplored_news_entities(): %s" % db.has_unexplored_news_entities())
        # the current collection round is over -> add new people
        if rounds + 1 == config["rounds"]: break
        extract_next_round_people(config, db)
        rounds += 1
    logger.success("NEXT_ROUND exited")

@logger.catch
def main():
    logger.success("Starting")
    config = parse_config("config.json")
    print(config)

    # load database
    db = get_db(config)
    logger.info("%sMB in db" % db.get_db_mb())

    # insert seed into db
    for s in config["seed"]:
        db.insert_person(s)
    # fix entities with bad label
    db.update_entities_to(config["actually_orgs"], "ORG")

    threads = [
        run_threaded(explore_news, config),
        run_threaded(explore_people, config),
        run_threaded(explore_entities, config),
        run_threaded(next_round, config)
    ]
    while threads[-1].is_alive(): # wait for next_round to complete
        time.sleep(1)  # join does not allow ctrl+c
    logger.success("Round execution finished, stopping")
    exit()



if __name__ == "__main__":
    main()
