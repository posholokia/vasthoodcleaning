from dataclasses import dataclass

import loguru
from services.crm.base import ICRM


@dataclass
class HouseProMockCRM(ICRM):
    def get_job_detail(self, job_id: str) -> dict:
        return self._request_get(job_id)

    def delete_schedule(self, job_id: str) -> None:
        """В моке не требует реализации"""
        # from services.crm.http_request.exceptions import HttpRequestError
        # raise HttpRequestError()
        loguru.logger.debug("Удален schedule у работы.")

    def add_delete_tag(self, job_id: str) -> None:
        """В моке не требует реализации"""
        # from services.crm.http_request.exceptions import HttpRequestError
        # raise HttpRequestError()
        loguru.logger.debug("Установлен тег 'delete' на работу.")

    @staticmethod
    def _request_get(job_id: str) -> dict:
        from .mock import job_orders

        return job_orders.get(job_id)
