import pickle
import os


CACHE_FILE = "market_cache.pkl"


def save_cache(data):
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(data, f)


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}

    with open(CACHE_FILE, "rb") as f:
        return pickle.load(f)

