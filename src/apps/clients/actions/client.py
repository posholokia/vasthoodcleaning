from dataclasses import dataclass

from apps.clients.models import (
    ClientEntity,
    CustomerModel,
)
from apps.clients.storage.base import IClientRepository


@dataclass
class ClientAction:
    """
    Обработка клиентских сценариев.
    """

    __client_repository: IClientRepository

    def create_if_not_exists(self, pk: str, phone: str) -> None:
        """
        Создать кастомера если он не существует.

        :param pk: id кастомера из crm
        :param phone: номер телефона кастомера
        :return: None
        """
        self.__client_repository.create_if_not_exists(pk=pk, phone=phone)

    def get_or_create(self, pk: str, phone: str) -> CustomerModel:
        """
        Получить кастомера или создать кастомера если он не существует.

        :param pk: id кастомера из crm
        :param phone: телефон кастомера
        :return: каcтомер dto
        """
        return self.__client_repository.get_or_create(pk, phone)

    def exists_customer(self, pk: str) -> bool:
        """
        Проверить, что кастомер существует.

        :param pk: id кастомера
        :return: bool
        """
        return self.__client_repository.exists(pk)

    def get_client(self, phone: str) -> ClientEntity:
        """
        Получить клиента по id.

        :param phone: номер телефона клиента.
        :return: ClientEntity
        """
        return self.__client_repository.get(phone)

    def delete_customer(self, pk: str) -> None:
        """
        Удаление кастомера.

        :param pk: id кастомера
        :return: None
        """
        return self.__client_repository.delete(pk=pk)
