from dataclasses import (
    dataclass,
    field,
)

from apps.clients.models import (
    ClientEntity,
    CustomerModel,
)
from apps.clients.storage.base import IClientRepository
from django.db import IntegrityError


@dataclass
class ORMClientRepository(IClientRepository):
    model: CustomerModel = field(init=False, default=CustomerModel)

    def create_if_not_exists(self, pk: str, phone: str) -> None:
        if not (self.model.objects.filter(pk=pk, phone=phone).exists()):
            try:
                self.model.objects.create(pk=pk, phone=phone)
            except IntegrityError:
                if not (
                    self.model.objects.filter(pk=pk, phone=phone).exists()
                ):
                    raise

    def get_or_create(self, pk: str, phone: str) -> CustomerModel:
        return self.model.objects.get_or_create(id=pk, phone=phone)[0]

    def get(self, phone: str) -> ClientEntity:
        orm_result = self.model.objects.filter(phone=phone)
        return ClientEntity(
            customer_ids=[customer.id for customer in orm_result],
            phone=phone,
        )

    def delete(self, pk: str) -> None:
        self.model.objects.delete(pk=pk)

    def exists(self, pk: str) -> bool:
        return self.model.objects.filter(pk=pk).exists()
