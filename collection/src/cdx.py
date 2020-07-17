# https://github.com/arquivo/pwa-technologies/wiki/URL-search:-CDX-server-API
# detect between each dates the news websites were crawled
import requests, json, os
from requests.exceptions import ReadTimeout
from urllib.parse import urlparse
from .utils import *


CACHE_FILE = abs_path("cdx_cache.json")
cache = open_cache(CACHE_FILE)


def netloc(website): return urlparse(website).netloc


def website_timeline(website, _from=1996, _to=2500):
    global cache
    nl = netloc(website)
    if nl in cache:
        return map(arquivo_date_str, cache[nl])

    url = "https://arquivo.pt/wayback/cdx"
    params = {
        "url": website,
        "from": _from,
        "to": _to,
        "output": "json"

    }
    try:
        r = requests.get(url, params, timeout=1)
    except ReadTimeout as e:
        logger.error("Timeout getting cdx for %s" % website)
        return

    captures = r.text.strip("\n").split("\n")

    def get_date(x): return json.loads(x)["timestamp"]
    _min = get_date(captures[0])
    _max = get_date(captures[-1])

    cache[nl] = (_min, _max)
    dict_to_json(cache, CACHE_FILE)
    return map(arquivo_date_str, [_min, _max])


def valid_website(site, _from, _to):
    _min, _max = website_timeline(site)
    return _to >= _min and _max >= _from

def get_valid_websites(websites, _from, _to):
    # skip if no collection exist for a given website
    res = []
    for site in websites:
        if valid_website(site, _from, _to):
            res.append(site)
    return res