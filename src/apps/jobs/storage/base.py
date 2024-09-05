from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from apps.jobs.models import JobStatus, JobEntity


@dataclass
class IJobRepository(ABC):
    @abstractmethod
    async def create(
        self,
        pk: str,
        schedule: datetime,
        address: str,
        status: JobStatus,
        total_cost: int,
        client_id: str,
        last_update: datetime,
    ): ...

    @abstractmethod
    async def list_by_client(self, client_phone: str) -> list[JobEntity]: ...

    @abstractmethod
    async def exists(self, pk) -> bool: ...

    @abstractmethod
    async def get_by_id(self, pk: str) -> JobEntity: ...

    @abstractmethod
    async def update(self, **kwargs) -> None: ...
