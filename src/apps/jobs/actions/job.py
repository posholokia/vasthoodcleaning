from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from apps.jobs.models import JobStatus, JobEntity
from apps.jobs.storage.base import IJobRepository
from loguru import logger


@dataclass
class WebhookJobAction:
    """
    Данные записываются по вебхукам, так как есть вероятность,
    что некоторые вкбхуки не придут или придут с задержкой,
    сценарии требуют дополнительных проверок и действий
    """
    __repository: IJobRepository
    date_format: str = field(init=False, default="%Y-%m-%dT%H:%M:%S%z")

    async def create(
        self,
        job_data: dict[str, Any],
    ) -> None:
        # проверяем что работы еще нет
        job_id = job_data["id"]
        if await self.__repository.exists(pk=job_id):
            return

        schedule = datetime.strptime(
            job_data["schedule"]["scheduled_start"],
            self.date_format
        )
        last_update = datetime.strptime(
            job_data["updated_at"],
            self.date_format
        )

        address = self._get_address_string(job_data["address"])
        logger.warning("test logger")
        # создаем работу
        await self.__repository.create(
            pk=job_id,
            schedule=schedule,
            address=address,
            status=JobStatus(job_data["work_status"]).value,
            total_cost=job_data["total_amount"],
            client_id=job_data["customer"]["id"],
            last_update=last_update,
        )

    async def get_list(self, client_phone: str) -> list[JobEntity]:
        return await self.__repository.list_by_client(client_phone)

    async def exists(self, pk: str) -> bool:
        return await self.__repository.exists(pk)

    async def update(self, job_data: dict) -> None:
        # получаем работу (уже должно быть проверено, что она существует)
        job = await self.__repository.get_by_id(job_data["id"])
        # сверяем дату последнего обновления в БД с текущими данными,
        # чтобы проверить актуальность данных
        new_update_datetime = datetime.strptime(
            job_data["updated_at"], self.date_format
        )
        if job.last_updated > new_update_datetime:
            return
        # если данные актуальны, обновляем работу
        job.total_cost = job_data["total_amount"]
        job.status = JobStatus(job_data["work_status"]).value
        job.address = self._get_address_string(job_data["address"])
        job.schedule = datetime.strptime(
            job_data["schedule"]["scheduled_start"],
            self.date_format
        )
        job.last_updated = new_update_datetime
        await self.__repository.update(
            pk=job.id,
            schedule=job.schedule,
            address=job.address,
            status=job.status,
            total_cost=job.total_cost,
            last_updated=job.last_updated,
        )

    @staticmethod
    def _get_address_string(address_dict: dict) -> str:
        street = address_dict["street"]
        street_line_2 = address_dict["street_line_2"]
        city = address_dict["city"]
        state = address_dict["state"]
        return f"{street} {street_line_2} {city} {state}"