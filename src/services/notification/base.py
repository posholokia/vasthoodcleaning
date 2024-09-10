from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Any


@dataclass
class INotificationReceiver(ABC):
    @abstractmethod
    def send(self, to_: str, message: str) -> None:
        """
        Отправить уведомление пользователю.

        :param to_: получатель сообщения
        :param message: текст сообщения
        :return: None
        """
