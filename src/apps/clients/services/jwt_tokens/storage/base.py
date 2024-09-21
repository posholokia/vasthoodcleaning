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

        :param key:     Подпись токена.
        :param value:   Токен.
        :param expire:  Временная метка окончания срока действия токена.
        :return:        Bool записан/не записан токен.
        """

    @abstractmethod
    def get_token(self, key: str):
        """
        Пытаемся получить токен из redis.

        :param key: Подпись токена.
        :return:    Токен или None.
        """
