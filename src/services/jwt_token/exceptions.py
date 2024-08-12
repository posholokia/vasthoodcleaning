class BaseJWTException(Exception):
    pass


class TokenTypeUndefined(BaseJWTException):
    pass


class InvalidTokenType(BaseJWTException):
    pass


class DecodeJWTError(BaseJWTException):
    pass


class TokenInBlacklistError(BaseJWTException):
    pass


class TokenExpireError(BaseJWTException):
    pass
