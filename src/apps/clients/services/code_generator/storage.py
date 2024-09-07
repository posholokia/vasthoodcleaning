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
    def save_code(self, phone: str, code: str) -> None: ...

    @abstractmethod
    def get_code(self, phone: str) -> str | None: ...

    @abstractmethod
    def delete_code(self, phone: str) -> None: ...


@dataclass
class RedisCodeStorage(ICodeStorage):
    conn: RedisPool
    code_exp: int = field(init=False, default=120)  # срок хранения кода

    def save_code(self, phone: str, code: str) -> None:
        redis = self.conn()
        saved = redis.set(
            name=phone,
            value=code,
            ex=self.code_exp,
        )
        if not saved:
            raise SaveCodeError()

    def get_code(self, phone: str) -> str | None:
        redis = self.conn()
        code: bytes = redis.get(phone)

        if code is None:
            return None

        return code.decode()

    def delete_code(self, phone: str) -> None:
        redis = self.conn()
        redis.delete(phone)
