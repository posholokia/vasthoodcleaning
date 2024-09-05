from django.http import HttpRequest
from ninja import Router
from loguru import logger

from api.v1.jobs.schema import JobSchema, JobDetailSchema
from core.security.jwt_auth import AuthBearer

router = Router(tags=["Jobs"])


@router.post("job/", response=None)
async def take_jobs(
    request: HttpRequest
) -> None:
    logger.warning(
        "CMS WEBHOOK: body: {}, header: {}",
        request.body,
        request.headers,
    )
    return None


@router.get(
    path="test_schema/",
    response=JobSchema,
    auth=AuthBearer(),
    description="Тест схемы",
)
async def test_schema(
    schema: JobSchema,
    request: HttpRequest,
) -> None:
    return None


@router.get(
    path="test_schema_detail/",
    response=JobDetailSchema,
    auth=AuthBearer(),
    description="Тест схемы",
)
async def test_schema_detail(
    schema: JobSchema,
    request: HttpRequest,
) -> None:
    return None
