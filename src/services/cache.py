import pickle
from datetime import timedelta
from typing import (
    Callable,
    ParamSpec,
    TypeVar,
)

from config.settings import conf
from services.redis_connection.connection import RedisPool


F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")


def cache_for_minutes(time_minutes: int = 1) -> Callable[F_Spec, F_Return]:
    """Простой декоратор для кеширования функций"""
    conn = RedisPool(conf.redis_db_cache)

    def decorator(
        func: Callable[F_Spec, F_Return],
    ) -> Callable[F_Spec, F_Return]:
        def wrapper(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return:
            cache = conn()
            key = pickle.dumps((func.__name__, args, kwargs))

            cached_func = cache.get(key)
            if cached_func:
                return pickle.loads(cached_func)

            res = func(*args, **kwargs)
            value = pickle.dumps(res)
            cache.set(key, value, ex=timedelta(minutes=time_minutes))
            return res

        return wrapper

    return decorator
