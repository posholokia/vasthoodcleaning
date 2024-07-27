from dataclasses import dataclass


@dataclass(eq=False)
class BaseHTTPException(Exception):
    code: int = 500
    message: str = "Непредвиденная ошибка приложения"
