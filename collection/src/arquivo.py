import requests, datetime
from .utils import *
from loguru import logger
    

def search_arquivo(query: str, _from: datetime, _to: datetime, websites: [str], max_items=2000, _type="html", fields="title,tstamp,originalURL,linkToNoFrame"):
    params = {
        "q": '"%s"' % query,
        "from": arquivo_date(_from),
        "to": arquivo_date(_to),
        "siteSearch": ",".join(websites),
        "fields": fields,
        "type": _type,
        "maxItems": max_items,
        "itemsPerSite": max_items//len(websites)
    }
    # itemsPerSite does not work
    return query_news(params, attempts=10)


def query_news(params, endpoint="https://arquivo.pt/textsearch", timeout=30, attempts=1):
    r = try_request(endpoint, params, timeout, attempts)
    if not r: return []
    return r.json()["response_items"]
