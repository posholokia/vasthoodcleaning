from dataclasses import dataclass

from apps.clients.services.jwt_tokens.storage.base import ITokenStorage
from loguru import logger
from services.redis_pool.connection import RedisPool


@dataclass
class RedisTokenStorage(ITokenStorage):
    conn: RedisPool

    async def set_token(
        self,
        key: str,
        value: str,
        expire: int | float,
        *args,
        **kwargs,
    ) -> bool:
        """
        key - подпись токена
        value - токен
        expire - временная метка окончания срока действия токена
        """
        redis = await self.conn()
        result: bool = await redis.set(
            name=key,
            value=value,
            exat=round(expire),
        )
        if not result:
            logger.error(
                "Не удалось записать ключ в Redis: {}: {}",
                key,
                value,
            )
        return result

    async def get_token(self, key: str, *args, **kwargs) -> str | None:
        redis = await self.conn()
        value: bytes = await redis.get(key)

        if value is None:
            return value

        return value.decode()