from dataclasses import dataclass

from services.crm.base import ICRM


@dataclass
class HouseProMockCRM(ICRM):
    def get_job_detail(self, job_id: str) -> dict:
        return self._request_get(job_id)

    @staticmethod
    def _request_get(job_id: str) -> dict:
        from .mock import job_orders

        return job_orders.get(job_id)
