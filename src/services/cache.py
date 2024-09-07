import pickle
from datetime import timedelta

from services.redis_pool.connection import RedisPool
from config.settings import conf


def cache_for_minutes(time_minutes: int = 1):
    conn = RedisPool(conf.redis_db_cache)

    def decorator(func):
        def wrapper(*args, **kwargs):
            cache = conn()
            key = pickle.dumps((hash(func), args, kwargs))

            cached_func = cache.get(key)
            if cached_func:
                return pickle.loads(cached_func)

            res = func(*args, **kwargs)
            value = pickle.dumps(res)
            cache.set(key, value, ex=timedelta(minutes=time_minutes))
            return res
        return wrapper
    return decorator
