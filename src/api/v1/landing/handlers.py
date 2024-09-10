from api.v1.landing.schema import (
    ServiceDetailRetrieveSchema,
    SiteRetrieveSchema,
)
from apps.landing.actions.actions import LandingAction
from django.http import HttpRequest
from ninja import Router
from core.mapper import dataclass_to_schema

from core.containers import get_container


router = Router(tags=["Landing"])


@router.get("site/", response=SiteRetrieveSchema)
def get_landing(request: HttpRequest) -> SiteRetrieveSchema:
    container = get_container()
    action: LandingAction = container.resolve(LandingAction)

    site = action.get_site()
    return dataclass_to_schema(obj=site, schema=SiteRetrieveSchema)


@router.get("service/{service_id}/", response=ServiceDetailRetrieveSchema)
def get_service(
    request: HttpRequest,
    service_id: int,
) -> ServiceDetailRetrieveSchema:
    container = get_container()
    action: LandingAction = container.resolve(LandingAction)

    service = action.get_service(service_id)
    return dataclass_to_schema(obj=service, schema=ServiceDetailRetrieveSchema)
