import json

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path
from ninja import NinjaAPI
from django.conf import settings

from config.containers import get_container
from core.constructor.exceptions import BaseHTTPException

from .v1.urls import router as v1_router
from loguru import logger


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
    container = get_container()
    return None


def get_webhooks(request: HttpRequest) -> HttpResponse:
    path = settings.BASE_DIR
    line_list = []
    with open(f"{path}/logs/warnings.log") as file:
        lines = file.readlines()[-10:]
        for line in lines:
            logger.info("{}", line)
            time, data = line.split("WARNING CMS WEBHOOK: body: b'")
            data = data.split("', header:")[0].rstrip(",\n").rstrip("'\n")
            line_list.append((time, json.loads(data.encode())))

    html = [dict_render(time_log=obj[0], data=obj[1]) for obj in line_list]
    return render(
        request,
        "index.html",
        {"data": [obj for obj in html]}
    )


def dict_render(data: dict[str, str | dict[str, str]],  time_log="", deep=0) -> str:
    logger.info("data: {} | {}", type(data), data)
    tab = " " * 4
    res = "{\n"

    time_log_line = f"<strong>{time_log}</strong>" if time_log else ""
    if isinstance(data, str):
        res += tab * (deep + 1) + data + "\n" + tab * deep + "}"
        return res
    deep += 1
    for key, value in data.items():
        res += tab * deep + f"{key}:  "

        if isinstance(value, dict):
            res += dict_render(value, deep=deep) + ",\n"
        elif isinstance(value, list):
            res += "["
            for item in value:
                res += "\n" + (tab * (deep+1)) + (dict_render(item, deep=deep+1) + ",\n" + tab * deep)
            res += "],\n"
        else:
            res += str(value) + ",\n"
    res += tab * (deep - 1) + "}"
    return time_log_line + res


api.add_router("v1/", v1_router)


urlpatterns = [
    path("", api.urls),
    path("webhooks/", get_webhooks)
]
