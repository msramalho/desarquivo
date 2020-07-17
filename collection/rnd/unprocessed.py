import sys
sys.path = ['.', '..', '../src'] + sys.path

from src.utils import *
from src.dbmongo import DbMongo, get_db


config = parse_config("config.json")
db = get_db(config)
print("%sMB in db" % db.get_db_mb())

status = {
    "unprocessed_people": db['people'].count_documents({"processed": {"$exists": False}}),
    "unprocessed_news": db['news'].count_documents({"processed": {"$exists": False}}),
    "unprocessed_news_entities": db['news'].count_documents({"processed_entities": {"$exists": False}, "valid": {"$exists": False}}),
    "most_mentioned": list(db.get_most_mentioned([], min_len=0))
}

for item in status.items():
    print("%s: %s" % item)