from dataclasses import dataclass, field
from django.db import IntegrityError

from apps.clients.models import ClientEntity, CustomerModel
from apps.clients.storage.base import IClientRepository


@dataclass
class ORMClientRepository(IClientRepository):
    model: CustomerModel = field(init=False, default=CustomerModel)

    async def create_if_not_exists(self, pk: str, phone: str) -> None:
        if not await (
                self.model.objects.
                filter(pk=pk, phone=phone)
                .aexists()
        ):
            try:
                await self.model.objects.acreate(pk=pk, phone=phone)
            except IntegrityError:
                if not await (
                        self.model.objects.
                        filter(pk=pk, phone=phone)
                        .aexists()
                ):
                    raise

    async def get(self, phone: str) -> ClientEntity:
        orm_result = await self.model.objects.filter(phone=phone)
        return ClientEntity(
            customer_ids=[customer.id for customer in orm_result],
            phone=phone,
        )

    async def delete(self, pk: str) -> None:
        await self.model.objects.adelete(pk=pk)

    async def exists(self, pk: str) -> bool:
        return await self.model.objects.filter(pk=pk).aexists()
