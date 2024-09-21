from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Any


@dataclass
class ICRM(ABC):
    @abstractmethod
    def get_job_detail(self, job_id: str) -> dict[str, Any]:
        """
        Получение детальной информации о заказанной работе из CRM.

        :param job_id:  ID работы в crm.
        :return:        Json с данными.
        """

    @abstractmethod
    def add_delete_tag(self, job_id: str) -> None:
        """
        Установка тега 'deleted' на работу.

        :param job_id:  ID работы.
        :return:        None.
        """

    @abstractmethod
    def delete_schedule(self, job_id: str) -> None:
        """
        Удаляет назначенное время из работы в CRM для освобождения календаря.

        :param job_id:  ID работы.
        :return:        None.
        """
