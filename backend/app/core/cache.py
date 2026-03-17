import time

_cache = {}

def cache_get(key):
    entry = _cache.get(key)
    if entry and time.time() < entry["expires"]:
        return entry["value"]
    return None

def cache_set(key, value, ttl=30):
    _cache[key] = {
        "value": value,
        "expires": time.time() + ttl
    }

redis_client = None