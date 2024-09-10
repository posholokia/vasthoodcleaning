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
        last_updated: datetime,
    ) -> None:
        """
        Создание работы

        :param pk: id работы из crm
        :param schedule: время начала работы
        :param address: адрес проведения работы
        :param status: статус работы
        :param total_cost: общая стоимость
        :param client_id: id кастомера, создавшего работу
        :param last_updated: дата последнего обновления
        :return: None
        """

    @abstractmethod
    def list_by_client(self, client_phone: str) -> list[JobEntity]:
        """
        Получить все работы по номеру телефона клиента,
        за исключением отмененных.

        :param client_phone: номер телефона клиента
        :return: список работ
        """

    @abstractmethod
    def exists(self, pk: str) -> bool:
        """
        Проверка, что работа существует по id.

        :param pk: id работы
        :return: bool
        """

    @abstractmethod
    def exists_by_client(self, pk: str, phone: str) -> bool:
        """
        Проверка, что эта работа указанного клиента

        :param pk: id работы.
        :param phone: номер телефона клиента
        :return: bool
        """

    @abstractmethod
    def get_by_id(self, pk: str) -> JobEntity | None:
        """
        Получить работу по id.

        :param pk: id работы
        :return: работа
        """

    @abstractmethod
    def update(self, **kwargs) -> None:
        """
        Обновить работу.

        :param kwargs: field_name: value, которые надо обновить
        :return: None
        """
