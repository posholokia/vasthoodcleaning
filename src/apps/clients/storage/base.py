from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from apps.clients.models import (
    ClientEntity,
    CustomerModel,
)


@dataclass
class IClientRepository(ABC):
    @abstractmethod
    def create_if_not_exists(self, pk: str, phone: str) -> None:
        """
        Записать кастомера в БД если он не существует.

        :param pk: первичный ключ кастомера
        :param phone: телефонный номер кастомера
        :return: None
        """

    @abstractmethod
    def get_or_create(self, pk: str, phone: str) -> CustomerModel:
        """
        Получить или создать кастомера если он не существует.

        :param pk: первичный ключ кастомера
        :param phone: телефонный номер кастомера
        :return: кастомер dto
        """

    @abstractmethod
    def get(self, phone: str) -> ClientEntity:
        """
        Получить клиента по номеру телефона.
        Объединяется из всех кастомеров с таким номером.

        :param phone: номер телефона
        :return: клиента
        """

    @abstractmethod
    def delete(self, pk: str) -> None:
        """
        Удалить одного кастомера по номеру телефона.

        :param pk: id кастомера
        :return: None
        """

    @abstractmethod
    def exists(self, pk: str) -> bool:
        """
        Проверяем что конкретный кастомер существует в БД

        :param pk: id кастомера
        :return: bool
        """
