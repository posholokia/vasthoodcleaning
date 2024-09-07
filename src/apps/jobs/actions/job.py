from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from apps.jobs.models import (
    JobStatus,
    JobEntity,
    JobDetailEntity,
    DiscountType,
)
from apps.jobs.services.parser import JobDetailJsonParser

from services.cache import cache_for_minutes
from apps.jobs.storage.base import IJobRepository
from loguru import logger

from services.crm.base import ICRM


@dataclass
class JobAction:
    """
    Данные записываются по вебхукам, так как есть вероятность,
    что некоторые вкбхуки не придут или придут с задержкой,
    сценарии требуют дополнительных проверок и действий
    """
    __repository: IJobRepository
    __crm_interface: ICRM
    __job_parser: JobDetailJsonParser
    date_format: str = field(init=False, default="%Y-%m-%dT%H:%M:%S%z")

    def create(
        self,
        job_data: dict[str, Any],
    ) -> None:
        # проверяем что работы еще нет
        job_id = job_data["id"]
        if self.__repository.exists(pk=job_id):
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
        self.__repository.create(
            pk=job_id,
            schedule=schedule,
            address=address,
            status=JobStatus(job_data["work_status"]).value,
            total_cost=job_data["total_amount"],
            client_id=job_data["customer"]["id"],
            last_update=last_update,
        )

    def get_list(self, client_phone: str) -> list[JobEntity]:
        return self.__repository.list_by_client(client_phone)

    @cache_for_minutes(1)
    def get_job_detail(self, job_id: str) -> JobDetailEntity:
        current_job = self.__repository.get_by_id(job_id)
        job_data = self.__crm_interface.get_job_detail(job_id)
        job_detail_entity = self.__job_parser.parse_data(job_data)

        job_cost = self._calculate_job_cost(job_detail_entity)
        if current_job.total_cost != job_cost:
            self.__repository.update(pk=job_id, total_cost=job_cost)
        return job_detail_entity

    @staticmethod
    def _calculate_job_cost(job: JobDetailEntity) -> int:
        parts = sum([part.cost for part in job.parts])
        materials = job.materials.total_cost
        discount = job.discount.value
        if job.discount.kind is DiscountType.fixed:
            return parts + materials - discount
        else:
            return round((parts + materials) * (1 - (discount / 10000)))

    def exists(self, pk: str) -> bool:
        return self.__repository.exists(pk)

    def update(self, job_data: dict) -> None:
        # получаем работу (уже должно быть проверено, что она существует)
        job = self.__repository.get_by_id(job_data["id"])
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
        self.__repository.update(
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