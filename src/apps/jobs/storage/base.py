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
        Проверка, что эта работа указанного клиента.

        :param pk:      ID работы.
        :param phone:   Номер телефона клиента.
        :return:        Bool.
        """

    @abstractmethod
    def get_by_id(self, pk: str) -> JobEntity | None:
        """
        Получить работу по id.

        :param pk:  ID работы.
        :return:    Работа.
        """

    @abstractmethod
    def update(self, pk: str, **kwargs) -> None:
        """
        Обновить работу.

        :param pk:      id работы.
        :param kwargs:  Поля, которые надо обновить.
                        Возможно обновить: schedule, address, status,
                        total_cost, paid, last_updated.
        :return:        None
        """

    @abstractmethod
    def delete(self, pk: str) -> None:
        """
        Удалить работу.

        :param pk:  id работы.
        :return:    None.
        """
