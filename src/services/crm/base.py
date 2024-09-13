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

        :param job_id: id работы в crm
        :return: json с данными
        """
