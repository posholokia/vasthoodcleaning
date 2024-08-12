from dataclasses import dataclass

from core.constructor.exceptions import BaseHTTPException


@dataclass(eq=False)
class InvalidCredentials(BaseHTTPException):
    code: int = 401
    message: str = "Invalid code or phone"


@dataclass(eq=False)
class NotExistsRefreshToken(BaseHTTPException):
    code: int = 400
    message: str = "Refresh token missing"


@dataclass(eq=False)
class JWTTokenInvalid(BaseHTTPException):
    code: int = 401
    message: str = "Token invalid, decode error"


@dataclass(eq=False)
class JWTTokenExpired(BaseHTTPException):
    code: int = 401
    message: str = "Token is expired"


@dataclass(eq=False)
class TokenInBlacklist(BaseHTTPException):
    code: int = 401
    message: str = "Token in blacklist"


@dataclass(eq=False)
class PhoneFormatError(BaseHTTPException):
    code: int = 400
    message: str = (
        "Invalid phone format, phone must "
        "start with + and contain 10-15 digits."
    )
