from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    datetime,
    UTC,
)

from apps.jobs.exceptions import CRMTemporarilyUnavailable
from apps.jobs.models import (
    DiscountType,
    JobDetailEntity,
    JobEntity,
    JobStatus,
)
from apps.jobs.services.parser import parse_job_detail
from apps.jobs.storage.base import IJobRepository
from services.cache import cache_for_minutes
from services.crm.base import ICRM
from services.crm.http_request import HttpRequestError


@dataclass
class JobAction:
    """
    Обработка сценариев связанных с работой.
    """

    __repository: IJobRepository
    __crm_interface: ICRM
    date_format: str = field(init=False, default="%Y-%m-%dT%H:%M:%S%z")

    def create(self, client_id: str, job: JobEntity) -> None:
        """
        Создание работы.

        :param job:         Сущность работы.
        :param client_id:   ID кастомера, создавшего работу.
        :return:            None.
        """
        # проверяем что работы еще нет
        if self.__repository.exists(pk=job.id):
            return

        # создаем работу
        self.__repository.create(
            pk=job.id,
            schedule=job.schedule,
            address=job.address,
            status=job.status,
            total_cost=job.total_cost,
            client_id=client_id,
            last_updated=job.last_updated,
        )

    def get_list(self, client_phone: str) -> list[JobEntity]:
        """
        Получить список работ клиента.

        :param client_phone:    Номер телефона клиента.
        :return:                Список работ.
        """
        jobs = self.__repository.list_by_client(client_phone)
        jobs.sort(key=lambda x: x.sort_by_schedule)
        return jobs

    @cache_for_minutes(1)
    def get_job_detail(self, job_id: str) -> JobDetailEntity:
        """
        Получить детальную информацию о заказанной работе.

        :param job_id:  ID работы.
        :return:        Детальная информация о работе.
        """
        current_job = self.__repository.get_by_id(job_id)
        try:
            job_data = self.__crm_interface.get_job_detail(job_id)
        except HttpRequestError:
            raise CRMTemporarilyUnavailable()
        job_detail_entity = parse_job_detail(job_data)

        job_cost = self._calculate_job_cost(job_detail_entity)
        if current_job.total_cost != job_cost:
            self.__repository.update(pk=job_id, total_cost=job_cost)
        return job_detail_entity

    @staticmethod
    def _calculate_job_cost(job: JobDetailEntity) -> int:
        """
        Перерасчет общей стоимости работы с учетом скидки.

        :param job: Детальная работа.
        :return:    Стоимость со скидкой.
        """
        discount = job.discount

        if not discount:
            return job.cost_before_discount

        if discount.kind is DiscountType.fixed:
            return job.cost_before_discount - discount.value
        else:
            return round(
                job.cost_before_discount * (1 - (discount.value / 10000))
            )

    def exists(self, pk: str) -> bool:
        """
        Проверка существует ли работа.

        :param pk:  ID работы.
        :return:    Bool.
        """
        return self.__repository.exists(pk)

    def update(self, job: JobEntity) -> None:
        """
        Обновление работы.

        :param job: Работа.
        :return:    None.
        """
        # получаем работу (уже должно быть проверено, что она существует)
        current_job = self.__repository.get_by_id(job.id)
        # сверяем дату последнего обновления в БД с текущими данными,
        # чтобы проверить актуальность данных
        if current_job.last_updated > job.last_updated:
            return
        # если данные актуальны, обновляем работу
        self.__repository.update(
            pk=job.id,
            schedule=job.schedule,
            address=job.address,
            status=job.status.value,
            total_cost=job.total_cost,
            paid=job.paid,
            last_updated=job.last_updated,
        )

    def delete(self, pk: str) -> None:
        """
        Удалить работу из БД.

        :param pk:  ID работы.
        :return:    None.
        """
        self.__repository.delete(pk)

    def cancel_job(self, job_id: str) -> None:
        """
        Отмена работы Клиентом.

        :param job_id:  ID работы.
        :return:        None.
        """

        self.__repository.update(
            pk=job_id,
            status=JobStatus.canceled.value,
            last_updated=datetime.now(UTC),
        )
        self.__crm_interface.delete_schedule(job_id)
        self.__crm_interface.add_delete_tag(job_id)
