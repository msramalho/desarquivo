import sys
sys.path = ['.', '..', '../src'] + sys.path

from src.utils import *
from src.dbmongo import DbMongo
from collections import defaultdict, Counter


def get_db(config):
    return DbMongo(config["mongodb"]["address"], config["mongodb"]["database"])

def is_subset(db, l1, l2):
    n1 = db["entities"].find_one({"_id": l1})["news"]
    n2 = db["entities"].find_one({"_id": l2})["news"]
    intersection = len((set(n1).intersection(n2)))
    return intersection/len(n1), intersection/len(n2)

def jaccard_index_query(db, l1, l2):
    n1 = db["entities"].find_one({"_id": l1})["news"]
    n2 = db["entities"].find_one({"_id": l2})["news"]
    intersection = len((set(n1).intersection(n2)))
    union = (len(n1) + len(n2)) - intersection
    print(intersection, union)
    return intersection / union

def jaccard_index(n1, n2):
    intersection = len((set(n1).intersection(n2)))
    union = (len(n1) + len(n2)) - intersection
    # print(intersection, union)
    return intersection / union

config = parse_config("config.json")
db = get_db(config)

# ingore = "', '".join("'dn,portugal,expresso-pt,diario-de-noticias,lusa,janeiro,fevereiro,março,marco,abril,maio,junho,julho,agosto,setembro,outubro,novembro,dezembro,'".split(","))
# for e1 in db["entities"].find({"$where": "this.label='PER'&&this.news.length>500&&![%s].includes(this.name)" % ingore}).limit(100):
#     for e2 in db["entities"].find().limit(100):
#         if e1["_id"] == e2["_id"]: continue
#         print(e1["_id"], e2["_id"], jaccard_index(e1, e2))


print(jaccard_index_query(db, "teixeira-dos", "teixeira-dos-santos"))
print(is_subset(db, "teixeira-dos", "teixeira-dos-santos"))
# print("-")
# print(jaccard_index_query(db, "socrates", "jose-socrates"))
# print(is_subset(db, "socrates", "jose-socrates"))
# print("-")
# print(jaccard_index(db, "ps", "psd"))
# print(jaccard_index(db, "ps", "partido-socialista"))
# print(is_subset(db, "ps", "partido-socialista"))
