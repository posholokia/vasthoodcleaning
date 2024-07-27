from dataclasses import dataclass

from services.constructor.exceptions import BaseHTTPException


@dataclass(eq=False)
class SiteNotFoundError(BaseHTTPException):
    code: int = 400
    message: str = "Site not found"


@dataclass(eq=False)
class ServiceNotFoundError(BaseHTTPException):
    code: int = 400
    message: str = "Service not found"
