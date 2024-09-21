from dataclasses import dataclass

from core.constructor.exceptions import BaseHTTPException


@dataclass(eq=False)
class CRMTemporarilyUnavailable(BaseHTTPException):
    code: int = 503
    message: str = "CRM is temporarily unavailable"
