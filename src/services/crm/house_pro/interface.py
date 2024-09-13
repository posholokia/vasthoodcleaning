from dataclasses import (
    dataclass,
    field,
)
from typing import Any

import httpx
from loguru import logger
from services.crm.base import ICRM
from services.crm.exceptions import CRMRequestError
from services.crm.house_pro.conf import (
    AUTH_HEADER,
    BASE_URL,
)


@dataclass
class HouseProCRM(ICRM):
    job_lines_path: str = field(init=False, default="jobs/{pk}/line_items")

    def get_job_detail(self, job_id: str) -> dict[str, Any]:
        path = self.job_lines_path.format(pk=job_id)
        return self._request_get(path)

    @staticmethod
    def _request_get(path: str) -> dict:
        url = f"{BASE_URL}{path}"
        with httpx.Client() as session:
            response = session.get(url=url, headers=AUTH_HEADER)
        if response.status_code > 400:
            logger.error(
                "Ошибка при отправке GET запроса в HouseCallPro. "
                "url: {}, header: {}, status: {}, response: {}",
                url,
                AUTH_HEADER,
                response.status_code,
                response.text,
            )
            raise CRMRequestError()
        return response.json()


if __name__ == "__main__":
    hcp = HouseProCRM()

    def main():
        hcp.get_job_detail("123")

    main()
"""
curl -X GET "https://api.housecallpro.com/customers" -H "Authorization: Token ca337b03477f45518e5851518c86c7e1"
curl -X GET "https://api.housecallpro.com/customers" -H "Authorization: Token 53922965ae0d4875a91a9ecb73f81b95"

curl -w "\nВремя выполнения: %{time_total} секунд\n" \
  --request GET \
  --url https://api.housecallpro.com/customers?q= \
  --header "Accept: application/json" \
  --header "Authorization: Token 53922965ae0d4875a91a9ecb73f81b95"
"""
