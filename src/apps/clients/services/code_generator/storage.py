from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass, field

from apps.clients.services.code_generator.exceptions import SaveCodeError
from services.redis_pool.connection import RedisPool


@dataclass
class ICodeStorage(ABC):
    @abstractmethod
    async def save_code(self, phone: str, code: str) -> None: ...

    @abstractmethod
    async def get_code(self, phone: str) -> str | None: ...

    @abstractmethod
    async def delete_code(self, phone: str) -> None: ...


@dataclass
class RedisCodeStorage(ICodeStorage):
    conn: RedisPool
    code_exp: int = field(init=False, default=120)  # срок хранения кода

    async def save_code(self, phone: str, code: str) -> None:
        redis = await self.conn()
        saved = await redis.set(
            name=phone,
            value=code,
            ex=self.code_exp,
        )
        if not saved:
            raise SaveCodeError()

    async def get_code(self, phone: str) -> str | None:
        redis = await self.conn()
        code: bytes = await redis.get(phone)

        if code is None:
            return None

        return code.decode()

    async def delete_code(self, phone: str) -> None:
        redis = await self.conn()
        await redis.delete(phone)
