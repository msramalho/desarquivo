import json, threading, os, re, requests, time
from slugify import slugify
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from loguru import logger
from collections import namedtuple

def run_threaded(job_func, *args, **kwargs):
    job_thread = threading.Thread(target=job_func, daemon=True, args=args, kwargs=kwargs)
    job_thread.start()
    return job_thread


def abs_path(filename):
    return "%s/%s" % (os.path.dirname(os.path.realpath(__file__)), filename)


def json_to_dict(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def dict_to_json(d, filename):
    with open(filename, "w", encoding="utf-8") as out:
        json.dump(d, out, ensure_ascii=False, indent=2)


def parse_date(date: str):
    return datetime.strptime(date, "%Y/%m/%d")


def split_between_dates(_from, _to, day_dif=365.4 * 2):
    # given two dates, return a list of tuples of at most one year length between them, covering the whole span
    delta = timedelta(days=day_dif)
    x = _from
    dates = []
    while x < _to:
        dates.append((x, min(_to, x + delta)))
        x += delta
    return dates


def parse_config(filename):
    config = json_to_dict(filename)
    config["from"] = parse_date(config["from"])
    config["to"] = parse_date(config["to"])
    return config


def arquivo_date(dt: datetime):
    return dt.strftime("%Y%m%d%H%M%S")


def arquivo_date_str(dt: str):
    return datetime.strptime(dt, "%Y%m%d%H%M%S")


def open_cache(filename):
    if os.path.isfile(filename):
        return json_to_dict(filename)
    return {}


def try_request(endpoint, params={}, timeout=30, attempts=10):
    r = None
    for i in range(attempts):
        try:
            r = requests.get(endpoint, params=params, timeout=timeout + (i * 5))
            if r.status_code == 404: return False
            if r.status_code == 429:  # too many requests
                time.sleep(10)
            if r.status_code != 200:
                raise Exception("Bad status code %s" % r.status_code)
            if 'Ã' in r.text and not "ç" in r.text:
                r.encoding = "utf-8"
            return r
        except Exception as e:
            logger.error("[%s] for [%s] (attempt %d/%d)" % (e, params, i + 1, attempts))
    if not r or r.status_code == 500: return False
    time.sleep(1)


def assert_valid_article(article):
    # assert newspaper3k did not go bad
    assert not re.match("Ao atingir o limite de artigos do Público Online", article.text), ("invalid %s" % article.text[:30])
    text = article.text
    # dn.pt is badly parsed
    if "Na sua opinião," in article.text: text = fix_dn(article)
    # expresso.sapo.pt
    if "<summary>" in article.html: text = fix_expresso(article)
    if "Assinar no iTunes" in article.text:
        text = article.text[:article.text.index("Assinar no iTunes")]
    text = text.strip()
    assert not "Todos os Blogues Expresso" in article.text, "Not an article"
    assert len(text) >= 150, ("News piece is too short [%s]" % text)
    assert len(text) < 10_000, ("News piece is too long %s" % len(text))
    return text


def fix_expresso(article):
    bs = BeautifulSoup(article.html, 'html.parser')
    try: return bs.find(id="artigo").find("summary").get_text()
    except: pass
    try: return bs.find(id="artigo").find("p", class_="newsP").get_text()
    except: pass
    return bs.find(id="artigo").get_text()


def fix_dn(article):
    bs = BeautifulSoup(article.html, 'html.parser')
    return bs.find(id="Article").get_text()


# setup clean_up_patterns

title_patterns_sub = [
    (re.compile(r"\?([A-zÀ-ÿ][A-zÀ-ÿ ]+)\?"), "\"\1\""),
    (re.compile(r"[“”″]+"), "\""),
    (re.compile(r"\"+"), "\""),
    (re.compile(r"^\"+(.*?)\"+$"), "\1")]

single = ["Expresso | ", "Visão | ", "dn - DN", "Cm ao Minuto - Correio da Manhã", " - Cm ao Minuto", " - Blogue DN", "Sol - ", " | Visão", "SOL : ", "Mais Sobre: ", " | Expresso", "Opinião: ", "Opinião. ", "a Sério", " - Tv Media", "JORNAL PUBLICO: ", "POL | Espaço Público | "]
bases = ["Sociedade", "Opinião", "Galerias", "Revistas", "Política", "Politica", "Tecnologia", "Tv & Media", "TV & Media", "Economia", "Bolsa", "Especiais", "Mundo", "Portugal", "Comentário", "Comentario", "Desporto", "Lusofonia", "Cultura", "Vida", "Angola", "Globo", "Farpas", "Investimento", "Liderança", "Energia"]
fins = ["DN", "PUBLICO.PT", "PÚBLICO", "CM", "Correio da Manhã", "Expresso.pt", "Sol", "Jornal de Notícias", "Visao.pt", "JN Live", "JN"]
forbidden_titles = {"DN - Diário de Notícias", "Object moved", "Meu JN", "Ficha Técnica", "Keydown.Dismiss", "Bs.Carousel", "V2.6", "Jwplayer.Vr", "Mouseup.Dismiss", "Piwik.Event", "Provider.Cast", "Submit.Validate", "Opinião", "Últimas Notícias"} | set(fins)


garbage = single
for b in bases:
    for f in fins:
        garbage.extend([b + " - " + f[:i] for i in range(1, len(f) + 1)][::-1])
    garbage.extend([b + " - ", b + " -", b + " "])
for f in fins:
    garbage.extend([" - " + f[:i] for i in range(1, len(f) + 1)][::-1])
for b in bases:
    garbage.extend([" - " + b[:i] for i in range(1, len(b) + 1)][::-1])


def clean_news_title_garbage(title):
    if title[0:7] == "http://": return " "
    if title[0:11] == "Mais Sobre: ": return " "
    if title in forbidden_titles: return " "
    title = title.strip().strip("-").strip("|").strip("_").strip()
    for pat, rep in title_patterns_sub:
        title = pat.sub(rep, title)
    for g in garbage:
        if g == title: return " "
        if g == title[:len(g)]: title = title[len(g):]
        if g == title[-len(g):]: title = title[:-len(g)]
    title = title.strip().strip("-").strip("|").strip("_").strip()
    # print(title)
    if not len(title): return " "  # to avoid crashes in the hash function
    if title in forbidden_titles: return " "
    return title


def set_from_tuples_list(l: list):
    keys = set()
    res = []
    for _id, _name in l:
        if _id not in keys:
            keys.add(_id)
            res.append((_id, _name))
    return res


def name_to_id(name: str):
    # "José Sócrates" -> jose-socrates
    return slugify(name)


NER = namedtuple("ner", "text,label_")


def ner_exceptions(text):
    res = []
    exceptions = [("Marinho e Pinto", "PER")]
    for e, label in exceptions:
        if e in text:
            res.append(NER(e, label))
    return res

# Duplicate entities detection


def jaccard_index(p1, p2):
    n1, n2 = p1["news"], p2["news"]
    intersection = len((set(n1).intersection(n2)))
    union = (len(n1) + len(n2)) - intersection
    return intersection / union


def is_subset(p1, p2):
    n1, n2 = p1["news"], p2["news"]
    intersection = len((set(n1).intersection(n2)))
    return intersection / len(n1), intersection / len(n2)


def contained_in(x, y):
    x1 = x.split("-")
    y1 = y.split("-")
    return all([p in y1 for p in x1]) or all([p in x1 for p in y1])


def is_duplicate(e1, e2):
    TH = 0.7  # threshold
    TH_match = 0.5  # threshold for when ids match
    # calculate metrics for decision
    s1, s2 = is_subset(e1, e2)
    ji = jaccard_index(e1, e2)

    # get individual names from entities
    p1 = set(e1["_id"].split("-"))
    p2 = set(e2["_id"].split("-"))
    # if one of them is contained in the other
    if contained_in(e1["_id"], e2["_id"]) and (s1 >= TH_match or s2 >= TH_match or ji >= TH_match) and ("-" in e1["_id"] or "-" in e2["_id"]) and ji > 0:
        pass  # accept
    else:
        if s1 < TH and s2 < TH and ji < TH: return False
        # if they overlap almost completely and have enough appearances in news pieces then they are considered to be the same
        if s1 >= 0.99 and s2 >= 0.99 and ji >= 0.99 and e1["len"] >= 15 and e2["len"] >= 15: pass
        elif s1 >= TH or s2 >= TH or ji >= TH:
            # otherwise they will only be duplicates if
            # * at least one of the three metrics is >= threshold
            # and one of the names is contained in the other
            # or their JaccardIndex is >= threshold and
            # they overlap except in one word and the smallest is not a single-word
            intersect = p1 & p2
            if not(intersect == p1 or intersect == p2 or
                    (ji >= TH and ((len(intersect) == len(p1) - 1 and len(p1) > 1) or
                                   (len(intersect) == len(p2) - 1 and len(p2) > 1)))
                   ):
                return False
    # from the two return the most relevant one for the future, meaning the one with the most appearances or, if the same, the largest one (more words)
    chosen = e1 if e1["len"] > e2["len"] else e2
    if e1["len"] == e2["len"]: chosen = e1 if len(p1) > len(p2) else e2
    logger.info("DUP [%s, %s, s1=%.2f, s2=%.2f, ji=%.2f] : %s" % (e1["_id"], e2["_id"], s1, s2, ji, chosen["_id"]))
    # return the chosen first and duplicate second
    if chosen["_id"] == e1["_id"]:
        return e1, e2
    return e2, e1
