import pymongo, re
from pymongo import UpdateOne, InsertOne
from urllib.parse import urlparse
from .utils import *
import hashlib


def get_db(config):
    return DbMongo(config["mongodb"]["address"], config["mongodb"]["database"])


class DbMongo():
    def __init__(self, mongo_address, database):
        self.mongo = pymongo.MongoClient(mongo_address)
        self.db = self.mongo[database]
        self.setup_db()

    def setup_db(self):
        # create indexes
        self["news"].create_index("_id_title", unique=True)
        self["news"].create_index("text", unique=True)

    def get_db_mb(self):
        return self.db.command("dbstats")["dataSize"] / (1024 * 1024)

    def get_unexplored_people(self):
        return self["people"].find({"processed": {"$exists": False}}, {"name": True}, no_cursor_timeout=True)

    def has_unexplored_people(self):
        return len(list(self.get_unexplored_people().limit(1)))

    def get_unexplored_news(self):
        return self["news"].find({"processed": {"$exists": False}, "valid": {"$exists": False}}, {"url": True, "entities": True}, no_cursor_timeout=True)

    def has_unexplored_news(self):
        return len(list(self.get_unexplored_news().limit(1)))

    def get_unexplored_news_entities(self):
        return self["news"].find({"processed_entities": {"$exists": False}, "valid": {"$exists": False}, "processed": True}, {"title": True, "text": True, "entities": True}, no_cursor_timeout=True)

    def has_unexplored_news_entities(self):
        return len(list(self.get_unexplored_news_entities().limit(1)))

    def upsert_news(self, news):
        if not len(news): return
        try: self["news"].bulk_write([InsertOne(n) for n in news], ordered=False)
        except pymongo.errors.BulkWriteError: pass  # ignore duplicate insertion errors
            

    def update_entities_to(self, ids, label):
        for e in ids:
            self._upsert_one("entities", {"_id": e, "label": label}, upsert=False)

    def update_entity_len(self):
        for e in self["entities"].find({}, no_cursor_timeout=True):
            e["len"] = len(e["news"]) if "news" in e else 0
            self._upsert_one("entities", e)

    def delete_ignored_people(self, ignore_people):
        self["people"].delete_many({"_id": {"$in": ignore_people}})

    def get_most_mentioned(self, ignore_ids, min_len=15, limit=200):
        # extract people that are not duplicates that have more than min_len appearances, and that have at least one dash "-" in their
        return self["entities"].find({"label": "PER", "duplicate_of": {"$exists": False}, "len": {"$gt": min_len}, "_id": {"$regex": ".+-.+", "$not": {"$in": ignore_ids}}}, {"name": True, "len": True, "text": True}, no_cursor_timeout=True).sort("len", -1).limit(limit)

    def get_explored_people_ids(self):
        return [p["_id"] for p in self["people"].find({"processed": True}, {}, no_cursor_timeout=True)]

    def _clean_news_piece(piece, query_person_id):
        # clean up bad encodings
        piece["title"] = clean_news_title_garbage(piece["title"])
        if piece["title"] == " ": return
        # clean
        piece["original"] = piece["originalURL"]
        del piece["originalURL"]
        piece["website"] = urlparse(piece["original"]).netloc
        piece["_id"] = hashlib.md5(piece["original"].encode('utf-8')).hexdigest()
        # id_title is a hash of website+title
        piece["_id_title"] = hashlib.md5((piece["website"] + piece["title"]).encode('utf-8')).hexdigest()
        piece["text"] = piece["_id_title"]  # temporarily must happen because of index on title
        piece["url"] = piece["linkToNoFrame"]
        del piece["linkToNoFrame"]
        piece["timestamp"] = arquivo_date_str(piece["tstamp"])
        del piece["tstamp"]
        # https://spacy.io/api/annotation#named-entities
        piece["entities"] = {"PER": [query_person_id], "LOC": [], "ORG": [], "MISC": []}
        return piece

    def upsert_news_piece(self, piece):
        try: self._upsert_one("news", piece)
        except:  # duplicate text error
            self["news"].delete_one({"_id": piece["_id"]})
            logger.error("Got duplicate text, deleting [%s]" % piece["_id"])

    def upsert_person(self, person):
        self._upsert_one("people", person)

    def upsert_people(self, people):
        if not len(people): return
        try: self["people"].bulk_write([UpdateOne({'_id': p['_id']}, {"$set": p}, upsert=True) for p in people], ordered=False)
        except pymongo.errors.BulkWriteError as e:
            logger.error("bulk error: %s" % e)

    def insert_person(self, name):
        person = {
            "_id": name_to_id(name),
            "name": self._clean_name(name)
        }
        self._upsert_one("people", person)

    def upsert_entities(self, entities):
        # {"_id":, "label":, "news": []}
        if not len(entities): return
        self["entities"].bulk_write([UpdateOne({'_id': e['_id']}, {
            "$set": {"label": e["label"], "text": e["text"]},
            "$addToSet": {"news": {"$each": e["news"]}}
        }, upsert=True) for e in entities], ordered=False)

    def _upsert_one(self, col, one, upsert=True):
        self[col].find_one_and_update({"_id": one["_id"]}, {"$set": one}, upsert=upsert)

    def _clean_name(self, name: str):
        # " José 2342   Sócrates " -> " José Sócrates "
        temp = re.sub(r"[^A-zÀ-ÿ ]+", "", name)
        temp = re.sub(r"^\s+|\s+$", "", temp)
        return re.sub(r" +", " ", temp)

    def __getitem__(self, colname):
        # allows reading self["col"] for collections
        return self.db[colname]

    def update_duplicate_entities(self, min_len=5, label="PER"):
        # TODO: this had to be loaded to memory since two inner cursors were not working
        entities = list(self["entities"].find({"label": label, "len": {"$gt": min_len}}, no_cursor_timeout=True))
        for i, p1 in enumerate(entities):
            for p2 in entities[i+1:]:
                res = is_duplicate(p1, p2)
                if not res: continue
                original, dup = res
                if "duplicate_of" in original: dup["duplicate_of"] = original["duplicate_of"]
                else: dup["duplicate_of"] = original["_id"]
                self._upsert_one("entities", dup)
                # self["entities"].find_one_and_update({"_id": dup["_id"]}, {"$addToSet": {"duplicate_of": {"$each": [original["_id"]]}}})
        self.update_duplicate_up_to_root(label)

    def update_duplicate_up_to_root(self, label):
        # resolve all duplicate_of to the root element, eg jose-socrates<-socrates<-ambiente-jose-socrates
        for e in self["entities"].find({"label": label, "duplicate_of": {"$exists": True}}, {"duplicate_of": True}, no_cursor_timeout=True):
            e["duplicate_of"] = self.get_duplicate_root(e)
            self._upsert_one("entities", e)

    def get_duplicate_root(self, e, depth=0):
        # climb up the duplicate_of dependency tree in search of root
        parent = self["entities"].find_one({"_id": e["duplicate_of"]}, {"duplicate_of": True})
        if depth >= 10:  # max recursion depth, otherwise assume loop
            logger.error("Found entity with loop in duplicate_of relation: [%s] AND [%s]" % (e["_id"], parent["_id"]))
            return parent["_id"]
        if "duplicate_of" in parent:
            return self.get_duplicate_root(parent, depth + 1)
        return parent["_id"]
