from django.http import HttpRequest
from ninja import Router

from api.v1.landing.schema import (
    ServiceDetailRetrieveSchema,
    SiteRetrieveSchema,
)
from apps.landing.actions.actions import LandingAction
from config.containers import get_container
from services.mapper import Mapper


router = Router(tags=["Landing"])


@router.get("site/", response=SiteRetrieveSchema)
async def get_landing(request: HttpRequest) -> SiteRetrieveSchema:
    container = get_container()
    action: LandingAction = container.resolve(LandingAction)

    site = await action.get_site()
    return Mapper.dataclass_to_schema(obj=site, schema=SiteRetrieveSchema)


@router.get("service/{service_id}/", response=ServiceDetailRetrieveSchema)
async def get_service(
    request: HttpRequest,
    service_id: int,
) -> ServiceDetailRetrieveSchema:
    container = get_container()
    action: LandingAction = container.resolve(LandingAction)

    service = await action.get_service(service_id)
    return Mapper.dataclass_to_schema(
        obj=service, schema=ServiceDetailRetrieveSchema
    )
