from dataclasses import dataclass

from apps.exceptions import ThisJobIsFromAnotherClient
from apps.jobs.storage.base import IJobRepository
from core.constructor.permissons import BasePermission


@dataclass(frozen=True, eq=False)
class JobPermissions(BasePermission):
    __repository: IJobRepository

    def has_permission(self, client_phone: str, job_id: str) -> None:
        if not self.__repository.exists_by_client(job_id, client_phone):
            raise ThisJobIsFromAnotherClient()
