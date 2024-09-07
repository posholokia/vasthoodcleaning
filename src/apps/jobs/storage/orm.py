from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime

from apps.jobs.models import (
    JobEntity,
    JobModel,
    JobStatus,
)
from apps.jobs.storage.base import IJobRepository


@dataclass
class ORMJobRepository(IJobRepository):
    model: JobModel = field(init=False, default=JobModel)

    def create(
        self,
        pk: str,
        schedule: datetime,
        address: str,
        status: JobStatus,
        total_cost: int,
        client_id: str,
        last_update: datetime | None = None,
    ):
        if last_update is None:
            last_update = datetime.now()
        self.model.objects.create(
            pk=pk,
            schedule=schedule,
            address=address,
            status=status,
            total_cost=total_cost,
            client_id=client_id,
            last_updated=last_update,
        )

    def list_by_client(self, client_phone: str) -> list[JobEntity]:
        orm_result = self.model.objects.filter(client__phone=client_phone)
        return [client.to_entity() for client in orm_result]

    def exists(self, pk) -> bool:
        return self.model.objects.filter(pk=pk).exists()

    def exists_by_client(self, pk: str, phone: str) -> bool:
        return self.model.objects.filter(pk=pk, client__phone=phone).exists()

    def get_by_id(self, pk: str) -> JobEntity:
        orm_result = self.model.objects.get(pk=pk)
        return orm_result.to_entity()

    def update(self, pk: str, **kwargs) -> None:
        self.model.objects.filter(pk=pk).update(**kwargs)
