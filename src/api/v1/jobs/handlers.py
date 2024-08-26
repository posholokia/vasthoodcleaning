from django.http import HttpRequest
from ninja import Router
from loguru import logger


router = Router(tags=["Jobs"])


@router.post("job/", response=None)
async def take_jobs(
    request: HttpRequest
) -> None:
    logger.warning("CMS WEBHOOK: {}", request.body)
    return None
