from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from apps.clients.models import ClientEntity


@dataclass
class IClientRepository(ABC):
    @abstractmethod
    def create_if_not_exists(self, pk: str, phone: str) -> None: ...

    @abstractmethod
    def get(self, phone: str) -> ClientEntity: ...

    @abstractmethod
    def delete(self, pk: str) -> None: ...

    @abstractmethod
    def exists(self, pk: str) -> bool: ...
