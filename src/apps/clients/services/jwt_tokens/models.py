from dataclasses import (
    dataclass,
    field,
)
from datetime import timedelta

from apps.clients.services.jwt_tokens.storage.base import ITokenStorage
from services.jwt_token.exceptions import (
    InvalidTokenType,
    TokenInBlacklistError,
)
from services.jwt_token.models import (
    Token,
    TokenType,
)


@dataclass
class AccessToken(Token):
    token_type: TokenType = TokenType.access
    lifetime: timedelta = timedelta(minutes=15)


@dataclass
class RefreshToken(Token):
    token_type: TokenType = TokenType.refresh
    lifetime: timedelta = timedelta(days=1)
    access_token_cls: AccessToken = field(default_factory=AccessToken)
    sub_claim: str = "client"

    def access_token(self, refresh_token: str) -> str:
        """Выдает access токен по refresh токену"""
        payload = self.decode(refresh_token)

        # проверяем что access токен обновляется по refresh токену
        if payload["typ"] != self.token_type.value:
            raise InvalidTokenType("Invalid refresh token type")

        self.access_token_cls.set_payload()
        self.access_token_cls[self.sub_claim] = payload[self.sub_claim]
        return self.access_token_cls.encode()

    def for_client(self, phone: str) -> str:
        """Выдаем refresh токен юзеру"""
        self.set_payload()
        self[self.sub_claim] = phone
        return self.encode()


@dataclass
class BlacklistRefreshToken(RefreshToken):
    """
    Refresh токен добавляется в черный список.
    Черный список хранится в хранилище, при выдаче нового access
    токена проверяем что его нет в черном списке, тогда
    выдаем токен. Бан осуществляется по подписи токена jti - uuid4.
    :: storage: хранилище забаненных токенов.
    """

    def __init__(self, storage: ITokenStorage):
        super().__init__()
        self.storage = storage

    def access_token(self, refresh_token: str) -> str:
        """Перед выдачей токена проверяем что его нет в черном списке"""
        self.check_blacklist(refresh_token)
        return super().access_token(refresh_token)

    def set_blacklist(self, token: str) -> None:
        """Записываем подпись токена в хранилище в черный список"""
        payload = self.decode(token)
        key = payload["jti"]
        timestamp_exp = payload["exp"]

        self.storage.set_token(
            key=key,
            value=token,
            expire=timestamp_exp,
        )

    def check_blacklist(self, token: str) -> None:
        """Проверяем, что токена нет в черном списке. Если есть, поднимаем ошибку"""
        payload = self.decode(token)
        value = self.storage.get_token(payload["jti"])

        if value is not None:
            raise TokenInBlacklistError("Tокен в черном списке")
