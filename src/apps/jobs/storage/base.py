from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from datetime import datetime

from apps.jobs.models import (
    JobEntity,
    JobStatus,
)


@dataclass
class IJobRepository(ABC):
    @abstractmethod
    def create(
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
    def list_by_client(self, client_phone: str) -> list[JobEntity]: ...

    @abstractmethod
    def exists(self, pk) -> bool: ...

    @abstractmethod
    def exists_by_client(self, pk: str, phone: str) -> bool: ...

    @abstractmethod
    def get_by_id(self, pk: str) -> JobEntity: ...

    @abstractmethod
    def update(self, **kwargs) -> None: ...
