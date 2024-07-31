from dataclasses import dataclass

from core.constructor.exceptions import BaseHTTPException


@dataclass(eq=False)
class InvalidProneNumber(BaseHTTPException):
    code: int = 400
    message: str = "Invalid phone number"
