from django.http import HttpRequest
from django.urls import path
from loguru import logger
from ninja import NinjaAPI

from core.constructor.exceptions import BaseHTTPException
from core.containers import get_container

from .v1.urls import router as v1_router


api = NinjaAPI()


@api.exception_handler(BaseHTTPException)
def return_exception(request, exc: BaseHTTPException):
    return api.create_response(
        request,
        data={"detail": exc.message},
        status=exc.code,
    )


@api.exception_handler(Exception)
def unhandled_exception(request, exc: Exception):
    # логирует необработанные ошибки
    logger.opt(exception=True).error("Debug error:")
    return api.create_response(
        request,
        data="Unhandled error",
        status=500,
    )


@api.get("/healthcheck")
def healthcheck(request: HttpRequest) -> None:
    get_container()
    return None


api.add_router("v1/", v1_router)


urlpatterns = [
    path("", api.urls),
]
