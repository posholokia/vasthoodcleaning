from dataclasses import dataclass

from django.db.models import Prefetch

from apps.landing.exceptions import (
    ServiceNotFoundError,
    SiteNotFoundError,
)
from apps.landing.models import (
    AboutBlock,
    Advantage,
    OurResultsPhoto,
    Question,
    Service,
    ServiceDetail,
    ServiceDetailEntity,
    Site,
    SiteEntity,
)
from apps.landing.services.storage.base import ISiteRepository
from services.mapper import Mapper


@dataclass
class ORMSiteRepository(ISiteRepository):
    async def get(self) -> SiteEntity:
        site = (
            await Site.objects.select_related(
                "about",
                "results",
                "main_screen",
                "footer",
                "faq",
            )
            .prefetch_related(
                Prefetch(
                    lookup="services",
                    queryset=Service.objects.select_related("font_color"),
                )
            )
            .prefetch_related(
                Prefetch(
                    lookup="about__blocks",
                    queryset=AboutBlock.objects.all(),
                )
            )
            .prefetch_related(
                Prefetch(
                    lookup="results__result_photos",
                    queryset=OurResultsPhoto.objects.all(),
                )
            )
            .prefetch_related(
                Prefetch(
                    lookup="faq__question",
                    queryset=Question.objects.all(),
                )
            )
            .afirst()
        )
        if site is None:
            raise SiteNotFoundError()
        return Mapper.model_to_dataclass(site, SiteEntity)

    async def get_service_detail(self, service_pk: int) -> ServiceDetailEntity:
        try:
            service = await (
                ServiceDetail.objects.select_related(
                    "service", "service__font_color"
                )
                .prefetch_related(
                    Prefetch(
                        lookup="advantage",
                        queryset=Advantage.objects.all(),
                    )
                )
                .aget(service_id=service_pk)
            )
        except ServiceDetail.DoesNotExist:
            raise ServiceNotFoundError()
        return Mapper.model_to_dataclass(service, ServiceDetailEntity)
