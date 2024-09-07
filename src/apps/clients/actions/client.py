from dataclasses import dataclass

from apps.clients.models import ClientEntity
from apps.clients.storage.base import IClientRepository


@dataclass
class ClientAction:
    __client_repository: IClientRepository

    def create_if_not_exists(self, customer_data: dict) -> None:
        self.__client_repository.create_if_not_exists(
            pk=customer_data["id"],
            phone=customer_data["mobile_number"]
        )

    def exists_customer(self, pk: str) -> bool:
        return self.__client_repository.exists(pk)

    def get_client(self, phone: str) -> ClientEntity:
        return self.__client_repository.get(phone)

    def delete_customer(self, customer_data: dict) -> None:
        return self.__client_repository.delete(pk=customer_data["id"])
