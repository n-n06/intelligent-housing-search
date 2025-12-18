import hashlib
from aiocache import RedisCache
from aiocache.serializers import JsonSerializer

cache = RedisCache(
    namespace="main",
    endpoint="redis",
    port=6379,
    ttl=60 * 60 * 24,
    serializer=JsonSerializer(),
)

def cache_key(prefix: str, value: str) -> str:
    return prefix + "_" + hashlib.md5(value.encode("utf-8")).hexdigest()
