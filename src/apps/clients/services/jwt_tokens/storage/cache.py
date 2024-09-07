from dataclasses import dataclass

from apps.clients.services.jwt_tokens.storage.base import ITokenStorage
from loguru import logger
from services.redis_pool.connection import RedisPool


@dataclass
class RedisTokenStorage(ITokenStorage):
    conn: RedisPool

    def set_token(
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
        redis = self.conn()
        result: bool = redis.set(
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

    def get_token(self, key: str, *args, **kwargs) -> str | None:
        redis = self.conn()
        value: bytes = redis.get(key)

        if value is None:
            return value

        return value.decode()
