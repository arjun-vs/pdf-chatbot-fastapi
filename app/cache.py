import time
import hashlib

CACHE_TTL = 300
CACHE = {}


def generate_cache_key(pdf_text: str, question: str) -> str:
    key_string = f"{pdf_text}-{question}"
    return hashlib.sha256(key_string.encode()).hexdigest()

def save_to_cache(key: str, value):
    CACHE[key] = (time.time(), value)

def get_from_cache(key: str):
    entry = CACHE.get(key)
    if entry:
        timestamp, value = entry
        timestamp = float(timestamp)
        if time.time() - timestamp < CACHE_TTL:
            return value
        else:
            del CACHE[key]
    return None

