import time
import uuid
from dataclasses import (
    dataclass,
    field,
)
from datetime import timedelta
from enum import Enum

import jwt
from config import settings
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
)
from loguru import logger
from core.jwt_token.exceptions import (
    DecodeJWTError,
    TokenExpireError,
    TokenTypeUndefined,
)


class TokenType(Enum):
    access: str = "access"
    refresh: str = "refresh"
    undefined: None = None


@dataclass
class Token:
    """Базовая модель jwt токена"""

    algorithm: str = "HS512"
    secret_key: str = settings.conf.crypto_key
    token_type: TokenType = TokenType.undefined
    _payload: dict = field(default_factory=dict)
    lifetime: timedelta = timedelta(days=1)

    def _set_exp(self, claim: str = "exp") -> None:
        self._payload[claim] = time.time() + self.lifetime.total_seconds()

    def _set_iat(self, claim: str = "iat"):
        self._payload[claim] = time.time()

    def _set_jti(self, claim: str = "jti"):
        self._payload[claim] = uuid.uuid4().hex

    def __setitem__(self, key, value):
        self._payload[key] = value

    def _set_type(self, claim: str = "typ"):
        if self.token_type == TokenType.undefined:
            raise TokenTypeUndefined(
                "Не указан тип токена, метод должен быть вызван "
                "в классе наследнике с указанием типа токена"
            )
        self._payload[claim] = self.token_type.value

    def set_payload(self):
        self._set_exp()
        self._set_iat()
        self._set_jti()
        self._set_type()

    def encode(self) -> str:
        if self.token_type == TokenType.undefined:
            raise TokenTypeUndefined(
                "Не указан тип токена, метод должен быть вызван "
                "в классе наследнике с указанием типа токена"
            )
        return jwt.encode(
            payload=self._payload,
            key=self.secret_key,
            algorithm=self.algorithm,
        )

    def decode(self, token) -> dict:
        try:
            payload = jwt.decode(
                jwt=token,
                key=self.secret_key,
                algorithms=[
                    self.algorithm,
                ],
                verify=True,
            )
        except DecodeError as e:
            logger.debug("Token decode error: {}", e)
            raise DecodeJWTError(f"Decode error: {e}")
        except ExpiredSignatureError:
            raise TokenExpireError("Срок действия токена истек")

        if payload.get("typ") is None:
            logger.debug("Missing token type")
            raise TokenTypeUndefined("Missing token type")

        return payload
