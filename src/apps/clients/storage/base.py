from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from apps.clients.models import ClientEntity


@dataclass
class IClientRepository(ABC):
    @abstractmethod
    async def create_if_not_exists(self, pk: str, phone: str) -> None: ...

    @abstractmethod
    async def get(self, phone: str) -> ClientEntity: ...

    @abstractmethod
    async def delete(self, pk: str) -> None: ...

    @abstractmethod
    async def exists(self, pk: str) -> bool: ...
