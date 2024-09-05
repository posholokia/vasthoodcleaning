from dataclasses import dataclass

from apps.clients.models import ClientEntity
from apps.clients.storage.base import IClientRepository


@dataclass
class WebhookClientAction:
    __client_repository: IClientRepository

    async def create_if_not_exists(self, customer_data: dict) -> None:
        await self.__client_repository.create_if_not_exists(
            pk=customer_data["id"],
            phone=customer_data["mobile_number"]
        )

    async def exists_customer(self, pk: str) -> bool:
        return await self.__client_repository.exists(pk)

    async def get_client(self, phone: str) -> ClientEntity:
        return await self.__client_repository.get(phone)

    async def delete_customer(self, customer_data: dict) -> None:
        return await self.__client_repository.delete(pk=customer_data["id"])
