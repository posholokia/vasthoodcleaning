from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from apps.landing.models import (
    ServiceDetailEntity,
    SiteEntity,
)


@dataclass
class ISiteRepository(ABC):
    @abstractmethod
    async def get(self) -> SiteEntity: ...

    @abstractmethod
    async def get_service_detail(
        self, service_pk: int
    ) -> ServiceDetailEntity: ...
