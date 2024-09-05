from dataclasses import dataclass

from apps.landing.models import (
    ServiceDetailEntity,
    SiteEntity,
)
from apps.landing.storage import ISiteRepository


@dataclass
class LandingAction:
    storage: ISiteRepository

    async def get_site(self) -> SiteEntity:
        return await self.storage.get()

    async def get_service(self, service_pk: int) -> ServiceDetailEntity:
        return await self.storage.get_service_detail(service_pk)
