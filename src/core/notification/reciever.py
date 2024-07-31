from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from core.notification.conf import NotificationConfig
from core.core

@dataclass
class INotificationReceiver(ABC):
    config: NotificationConfig

    @abstractmethod
    async def connect(self, config: dict) -> Any: ...

    @abstractmethod
    async def receive(self, *args, **kwargs) -> None: ...
