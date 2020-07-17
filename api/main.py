from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from py2neo import Graph
from loguru import logger
# https://stackoverflow.com/a/53918402/6196010
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
#app.debug = True  # TODO: update in production

CORS(app)

print("DEBUG? %s" % app.debug)

app.config["MONGO_SERVER_SELECTION_TIMEOUT_MS"] = 1000 * 60 * 60 # 1h
if app.debug:
    app.config["MONGO_URI"] = "mongodb://localhost:27017/" + "admin"
    graph = Graph("bolt://localhost:7687")
else:  # docker version
    app.config["MONGO_URI"] = "mongodb://mongo:27017/" + "admin"
    graph = Graph("bolt://neo4j:7687")

mongo = PyMongo(app)
db = mongo.cx.get_database("desarquivo")
col_news = db.get_collection("final_news")
col_entities = db.get_collection("final_entities")
col_entities.create_index([('search_text', 'text')])
col_news.create_index('timestamp')  # for sorting operations


convert_labels = {"PER": "Pessoa", "ORG": "Organização", "LOC": "Local", "MISC": "Outros"}


@app.route("/")
def alive():
    return {"alive": True}


def prepare_entity_for_frontend(e):
    e["label_pt"] = convert_labels[e["label"]]
    return e


@app.route("/search")
def search():
    # get query -> return full text search on entities (will do exact match and not term split)
    query = request.args.get('query')
    query = "%3s" % query
    return {"results": list(map(prepare_entity_for_frontend, col_entities.find({"$text": {"$search": '"%s"' % query, "$caseSensitive": False, "$diacriticSensitive": False}}, {"label": True, "text": True, 'score': {'$meta': 'textScore'}}).sort([('score', {'$meta': 'textScore'})]).limit(10)))}


def add_labels(node_name="n"):
    labels = request.args.get('labels')
    if labels:
        labels = labels.split(",")
        return " WHERE " + " OR ".join(["%s:%s" % (node_name, l) for l in labels])
    return ""


@app.route("/expand")
def expand():
    # get entity._id, [limit] -> return sorted (if limit else all) list of connections
    # TODO: include label?
    _id = request.args.get('_id')
    limit = request.args.get('limit')
    if not _id: return "Invalid Id", 500
    # TODO: update injection when py2neo becomes decent...
    q = "MATCH ({_id:'%s'})-[r:rel]-(n)" % _id
    q += add_labels()
    q += " RETURN r, n, labels(n)"
    try: q += " ORDER BY r.weight DESC LIMIT %d" % int(limit)
    except: pass
    res = []
    for r in graph.run(q):
        d = r[1]
        d["weight"] = r[0]["weight"]
        d["label"] = r[2][0]
        res.append(d)
    return {"connections": res}
    # return {"connections": list(graph.run(q))}
    # node = graph.nodes.match(_id=_id).first()
    # return {"relationships": list(graph.relationships.match((node, None), "rel").limit(3))}


def split_news_intervals(news):
    # returns list of parts (id, timestamp, index in original)
    max_parts = 20
    ideal_parts_len = 100
    # len=100 -> 1 part, len=200 -> 2 part, len=4000 -> 20 part (max)
    parts = max(1, min(max_parts, len(news) // ideal_parts_len))
    parts_len = len(news) // parts
    # return [(n["_id"], int(n["timestamp"].timestamp()), i*parts_len) for i, n in enumerate(news[::parts_len])]
    return [(n["_id"], n["timestamp"], i * parts_len) for i, n in enumerate(news[::parts_len])]


def sort_news(news_ids):
    try:
        news = list(col_news.find({"_id": {"$in": news_ids}}, {"timestamp": True}).sort("timestamp", -1))
        return {"news_ids": [n["_id"] for n in news], "parts": split_news_intervals(news)}
    except Exception as e:
        print(e)
        return {"news_ids": [], "parts": []}


def news_between(_from, _to):
    pipeline = [
        {"$match": {"_id": {"$in": [_from, _to]}}},
        {"$group": {"_id": 0, "s0": {"$first": "$news"}, "s1": {"$last": "$news"}}},
        {"$project": {"_id": 0, "news_ids": {"$setIntersection": ["$s0", "$s1"]}}}
    ]
    return next(col_entities.aggregate(pipeline))["news_ids"]


@app.route("/edge_news")
def edge_news():
    # get from, to entities -> return list of news_ids between them sorted by date (newer first)
    _from = request.args.get('from')
    _to = request.args.get('to')
    if not _from or not _to: return "invalid edge information", 500
    try:
        return sort_news(news_between(_from, _to))
    except Exception as e:
        print(e)
        return {"news_ids": []}


@app.route("/entity_news")
def entity_news():
    # get entity _id -> return list of news_ids sorted by date (newer first)
    # after testing I concluded that aggregate (match,project,lookup,project,sort)
    # takes twice as long as 2 queries: 1 to get news_ids, another to sort them (even for large ones > 7k news)
    _id = request.args.get('_id')
    if not _id: return "Invalid Id", 500
    try:
        return sort_news(col_entities.find_one({"_id": _id}, {"news": True})["news"])
    except Exception as e:
        print(e)
        return {"news_ids": []}


@app.route("/news")
def news():
    # get news_ids -> return list of news documents
    # ideally this will be paged (batches of news to avoid too much data max 20 at a time)
    try: news_ids = request.args.get('news_ids').split(",")[:20]
    except: return "invalid news_ids", 500
    return {"news": list(col_news.find({"_id": {"$in": news_ids}}, {"entities": True, "image": True, "text": True, "title": True, "url": True, "timestamp": True}).sort("timestamp", -1))}


@app.route("/connections")
def connections():
    # get from, to -> return list of nodes that are connected to both
    _from = request.args.get('from')
    _to = request.args.get('to')
    if not _from or not _to: return "invalid nodes information (from, to) required", 500

    q = 'MATCH (x{_id:"%s"})-[r1]-(n)-[r2]-(y{`_id`:"%s"})' % (_from, _to)
    q += add_labels()
    q += ' RETURN r1, n, r2, labels(n)'
    try: q += " ORDER BY (r1.weight + r2.weight) DESC LIMIT %d" % int(request.args.get('limit'))
    except: pass
    res = []
    for r in graph.run(q):
        d = r[1]
        d["from"] = r[0]["weight"]
        d["to"] = r[2]["weight"]
        d["label"] = r[3][0]
        res.append(d)
    return {"connections": res}


@app.route("/connection")
def connection():
    # get from, to -> return list of nodes that are connected to both
    _from = request.args.get('from')
    _to = request.args.get('to')
    if not _from or not _to: return "invalid nodes information (from, to) required", 500
    try: return {"weight": len(news_between(_from, _to))}
    except: return {"weight": 0}


@app.after_request
def add_header(response):
    response.cache_control.max_age = 54000  # 15min
    response.cache_control.public = True
    logger.info(request.full_path)
    return response


if __name__ == '__main__':
    logger.remove()
    logger.add("logs.txt", format="{time:X}|{message}", level="INFO")
    # Debug/Development
    # app.run(debug=True, host='0.0.0.0')
    # Production
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
