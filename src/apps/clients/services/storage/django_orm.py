from dataclasses import dataclass

from apps.clients.models.orm import ClientModel
from apps.clients.services.storage.base import IClientRepository


@dataclass
class ORMClientRepository(IClientRepository):
    model: ClientModel = ClientModel

    async def get_or_create(self, phone: str) -> model:
        return self.model.objects.aget_or_create(phone=phone)
