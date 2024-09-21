from dataclasses import dataclass

from core.constructor.exceptions import BaseHTTPException


@dataclass(eq=False)
class TooOftenSendingError(BaseHTTPException):
    code: int = 400
    message: str = "Code sent too often, 60 seconds must pass before resending"


@dataclass(eq=False)
class SaveCodeError(BaseHTTPException):
    code: int = 503
    message: str = "Failed to save verification code"


class CodeMatchError(Exception):
    pass
