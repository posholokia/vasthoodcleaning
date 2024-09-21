import time
from typing import (
    Callable,
    ParamSpec,
    TypeVar,
)

import httpx

from .exceptions import HttpRequestError


F_Return = TypeVar("F_Return")
F_Spec = ParamSpec("F_Spec")


def retry(func: Callable[F_Spec, F_Return]) -> Callable[F_Spec, F_Return]:
    def wrapper(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return:
        for i in range(3):
            try:
                return func(*args, **kwargs)
            except httpx.ReadTimeout:
                time.sleep(1)
        raise HttpRequestError("Сервис недоступен")

    return wrapper
