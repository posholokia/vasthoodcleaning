import math
from dataclasses import dataclass, field

import httpx

from apps.clients.models import ClientEntity
from services.crm.house_mock.utils import convert_data_to_dto, get_from_all_pages
from services.crm.house_pro.dto import CustomerDTO
from services.crm.house_pro.conf import BASE_URL, AUTH_HEADER
from loguru import logger

from services.crm.exceptions import CRMRequestError


@dataclass
class HouseProInterface:
    customers_path: str = field(init=False, default="customers")

    async def get_client(self, number: str) -> ClientEntity:
        _, customers = await self._get_customer_page(
            self.customers_path, query=number,
        )
        return ClientEntity(
            customer_ids=[customer.id for customer in customers],
            phone=number
        )

    async def get_client_jobs(self, client: ClientEntity):
        ...

    @get_from_all_pages
    async def _get_customer_page(
        self,
        path: str,
        query: str,
        page: int = 1,
        page_size: int = 3,
    ) -> tuple[int, list[CustomerDTO]]:
        result = await self._request_get(path, query, page, page_size)
        total_pages = result["total_pages"]
        customers = [
            convert_data_to_dto(customer) for customer in result["customers"]
        ]
        return total_pages, customers

    async def _request_get(
        self,
        path: str,
        query: str = "",
        page: int = 1,
        page_size: int = 3,
    ) -> dict:
        from services.crm.house_mock.mock import customers as customer_storage
        if path == self.customers_path:
            customers = customer_storage[(page - 1) * page_size: page * page_size]
            total_items = len(customer_storage)
            total_pages = math.ceil(total_items / page_size)
            if query:
                customer_filter = filter(
                    lambda x: x["mobile_number"] == query, customers
                )
                customers = [customer for customer in customer_filter]
            response = {
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "total_items": total_items,
                "customers": customers
            }
            return response
        return {}


if __name__ == '__main__':
    import asyncio

    hcp = HouseProInterface()

    async def main():
        res = await hcp.get_client("3126848315")
        print(res)

    asyncio.run(main())
"""
curl -X GET "https://api.housecallpro.com/customers" -H "Authorization: Token ca337b03477f45518e5851518c86c7e1"
curl -X GET "https://api.housecallpro.com/customers" -H "Authorization: Token 53922965ae0d4875a91a9ecb73f81b95"

curl -w "\nВремя выполнения: %{time_total} секунд\n" \
  --request GET \
  --url https://api.housecallpro.com/customers?q= \
  --header "Accept: application/json" \
  --header "Authorization: Token 53922965ae0d4875a91a9ecb73f81b95"
"""