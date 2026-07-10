import os
import pickle


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CACHE_FILE = os.path.join(BASE_DIR, "market_cache.pkl")


def save_cache(data):
    try:
        with open(CACHE_FILE, "wb") as f:
            pickle.dump(data, f)
    except Exception as e:
        print(f"Ошибка сохранения cache: {e}")


def load_cache():
    try:
        if not os.path.exists(CACHE_FILE):
            return {}

        with open(CACHE_FILE, "rb") as f:
            return pickle.load(f)

    except Exception as e:
        print(f"Ошибка загрузки cache: {e}")
        return {}

