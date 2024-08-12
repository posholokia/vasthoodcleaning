from dataclasses import dataclass

from config.settings import CONF
from redis import asyncio as aioredis


@dataclass
class RedisPool:
    db_number: int

    async def __call__(self) -> aioredis.Redis:
        conn = aioredis.Redis(
            host=CONF.redis_host,
            username=CONF.redis_user,
            password=CONF.redis_pass,
            port=CONF.redis_port,
            db=self.db_number,
        )
        return conn
