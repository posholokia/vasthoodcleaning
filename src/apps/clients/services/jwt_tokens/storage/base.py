from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class ITokenStorage(ABC):
    """
    Хранилище jwt refresh токенов
    """

    @abstractmethod
    def set_token(self, key: str, value: str, expire: int | float):
        """
        Записывает токен в redis

        :param key: подпись токена
        :param value: токен
        :param expire: временная метка окончания срока действия токена
        :return: bool записан/не записан токен
        """

    @abstractmethod
    def get_token(self, key: str):
        """
        Пытаемся получить токен из redis

        :param key: подпись токена
        :return: токен или None
        """
