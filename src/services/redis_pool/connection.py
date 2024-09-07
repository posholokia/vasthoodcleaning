import redis
from dataclasses import dataclass

from config.settings import conf


@dataclass
class RedisPool:
    db_number: int

    def __call__(self) -> redis.Redis:
        conn = redis.Redis(
            host=conf.redis_host,
            username=conf.redis_user,
            password=conf.redis_pass,
            port=conf.redis_port,
            db=self.db_number,
        )
        return conn
