from dataclasses import dataclass, field
from datetime import datetime

from apps.jobs.models import JobStatus, JobEntity, JobModel
from apps.jobs.storage.base import IJobRepository


@dataclass
class ORMJobRepository(IJobRepository):
    model: JobModel = field(init=False, default=JobModel)

    async def create(
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
        await self.model.objects.acreate(
            pk=pk,
            schedule=schedule,
            address=address,
            status=status,
            total_cost=total_cost,
            client_id=client_id,
            last_updated=last_update,
        )

    async def list_by_client(self, client_phone: str) -> list[JobEntity]:
        orm_result = await self.model.objects.filter(client__phone=client_phone)
        return [client.to_entity() for client in orm_result]

    async def exists(self, pk) -> bool:
        return await self.model.objects.filter(pk=pk).aexists()

    async def get_by_id(self, pk: str) -> JobEntity:
        orm_result = await self.model.objects.aget(pk=pk)
        return orm_result.to_entity()

    async def update(self, pk: str, **kwargs) -> None:
        await self.model.objects.filter(pk=pk).aupdate(**kwargs)
