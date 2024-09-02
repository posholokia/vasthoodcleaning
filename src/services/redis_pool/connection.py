from dataclasses import dataclass

from config.settings import conf
from redis import asyncio as aioredis


@dataclass
class RedisPool:
    db_number: int

    async def __call__(self) -> aioredis.Redis:
        conn = aioredis.Redis(
            host=conf.redis_host,
            username=conf.redis_user,
            password=conf.redis_pass,
            port=conf.redis_port,
            db=self.db_number,
        )
        return conn
