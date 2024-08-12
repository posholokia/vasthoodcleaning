from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from apps.clients.models.orm import ClientModel


@dataclass
class IClientRepository(ABC):
    @abstractmethod
    async def get_or_create(self, phone: str) -> ClientModel: ...
