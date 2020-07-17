# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from src.utils import *
from src.dbmongo import DbMongo, get_db
from collections import defaultdict, Counter
from loguru import logger


# %%
config = parse_config("config.json")
db = get_db(config)

# %% [markdown]
# ## Check if any website is providing little results

# %%
from collections import Counter


# %%
ws = [n["website"] for n in db["news"].find({"valid": {"$exists": False}, "processed": True}, {"website": 1})]


# %%
Counter(ws).most_common(1000)

