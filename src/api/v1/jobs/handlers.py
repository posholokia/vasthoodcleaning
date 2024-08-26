from django.http import HttpRequest, HttpResponse
from ninja import Router
from loguru import logger
from django.shortcuts import render


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
