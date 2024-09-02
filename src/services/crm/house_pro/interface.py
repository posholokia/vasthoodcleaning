from dataclasses import dataclass, field

import httpx

from services.crm.house_pro.dto import CustomerDTO
from services.crm.house_pro.conf import BASE_URL, AUTH_HEADER
from loguru import logger

from services.crm.exceptions import CRMRequestError


@dataclass
class HouseProInterface:
    customers_path: str = field(init=False, default="customers")

    async def get_customers(self, number: str = "") -> CustomerDTO:
        query = f"{number}"
        response = await self._request_get(self.customers_path, query)
        print(response)

    async def _request_get(self, path: str, query: str = "") -> dict:
        url = f"{BASE_URL}{path}?q={query}"
        async with httpx.AsyncClient() as session:
            response = await session.get(
                url=url,
                headers=AUTH_HEADER,
            )
            if response.status_code != 200:
                logger.error(
                    "Ошибка при отправке GET запроса в HouseCallPro. "
                    "url: {}, header: {}, query: {}, status: {}, response: {}",
                    url, AUTH_HEADER, query, response.status_code, response.text,
                )
                raise CRMRequestError()
            return response.json()


if __name__ == '__main__':
    import asyncio

    hcp = HouseProInterface()

    async def main():
        await hcp.get_customers()

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