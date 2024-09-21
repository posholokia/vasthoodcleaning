from dataclasses import (
    dataclass,
    field,
)
from typing import Any

from apps.jobs.models import DeleteTag
from services.crm.base import ICRM
from services.crm.house_pro.conf import (
    AUTH_HEADER,
    BASE_URL,
)
from services.crm.http_request import HttpRequest


@dataclass
class HouseProCRM(ICRM):
    _requester: HttpRequest
    job_lines_path: str = field(init=False, default="jobs/{pk}/line_items")
    job_tag_path: str = field(
        init=False, default="jobs/{job_id}/tags?tag_id={tag_id}"
    )
    jod_schedule_path: str = field(
        init=False, default="jobs/{job_id}/schedule"
    )

    def get_job_detail(self, job_id: str) -> dict[str, Any]:
        path = self.job_lines_path.format(pk=job_id)
        url = f"{BASE_URL}{path}"
        response = self._requester.get(url, header=AUTH_HEADER)
        return response.json()

    def add_delete_tag(self, job_id: str) -> None:
        path = self.job_tag_path.format(job_id=job_id, tag_id=DeleteTag.id)
        url = f"{BASE_URL}{path}"
        self._requester.post(url, body=None, header=AUTH_HEADER)

    def delete_schedule(self, job_id: str) -> None:
        path = self.jod_schedule_path.format(job_id=job_id)
        url = f"{BASE_URL}{path}"
        self._requester.delete(url, header=AUTH_HEADER)


if __name__ == "__main__":
    hcp = HouseProCRM(HttpRequest())

    def main():
        hcp.add_delete_tag("job_dd33d292af724545bd190d055c97423d")

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
