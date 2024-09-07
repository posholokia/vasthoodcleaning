from dataclasses import dataclass

from apps.landing.models import (
    AboutBlock,
    Advantage,
    FAQ,
    OurResultsPhoto,
    Service,
    ServiceDetail,
    ServiceDetailEntity,
    Site,
    SiteEntity,
)
from apps.landing.exceptions import (
    ServiceNotFoundError,
    SiteNotFoundError,
)
from apps.landing.storage import ISiteRepository
from django.db.models import Prefetch
from services.mapper import Mapper


@dataclass
class ORMSiteRepository(ISiteRepository):
    def get(self) -> SiteEntity:
        site = (
            Site.objects.select_related(
                "about",
                "results",
                "main_screen",
                "footer",
            )
            .prefetch_related(
                Prefetch(
                    lookup="services",
                    queryset=Service.objects.select_related(
                        "font_color"
                    ).order_by("id"),
                )
            )
            .prefetch_related(
                Prefetch(
                    lookup="about__blocks",
                    queryset=AboutBlock.objects.all().order_by("id"),
                )
            )
            .prefetch_related(
                Prefetch(
                    lookup="results__result_photos",
                    queryset=OurResultsPhoto.objects.all().order_by("id"),
                )
            )
            .prefetch_related(
                Prefetch(
                    lookup="faq",
                    queryset=FAQ.objects.all().order_by("id"),
                )
            )
            .first()
        )
        if site is None:
            raise SiteNotFoundError()
        return Mapper.model_to_dataclass(site, SiteEntity)

    def get_service_detail(self, service_pk: int) -> ServiceDetailEntity:
        try:
            service = (
                ServiceDetail.objects.select_related(
                    "service", "service__font_color"
                )
                .prefetch_related(
                    Prefetch(
                        lookup="advantage",
                        queryset=Advantage.objects.all().order_by("id"),
                    )
                )
                .get(service_id=service_pk)
            )
        except ServiceDetail.DoesNotExist:
            raise ServiceNotFoundError()
        return Mapper.model_to_dataclass(service, ServiceDetailEntity)
