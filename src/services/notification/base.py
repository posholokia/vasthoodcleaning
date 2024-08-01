from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class INotificationReceiver(ABC):
    @abstractmethod
    async def connect(self) -> Any: ...
    @abstractmethod
    async def receive(self, data: dict) -> None: ...
