from dataclasses import dataclass

from core.constructor.exceptions import BaseHTTPException


@dataclass(eq=False)
class ThisJobIsFromAnotherClient(BaseHTTPException):
    code: int = 403
    message: str = "This job is from another client"
