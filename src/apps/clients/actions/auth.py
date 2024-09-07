from dataclasses import dataclass

from apps.clients.exceptions import (
    InvalidCredentials,
    JWTTokenExpired,
    JWTTokenInvalid,
    SmsServiceError,
    TokenInBlacklist,
)
from apps.clients.services.code_generator.code import VerificationCodeService
from apps.clients.services.jwt_tokens.models import BlacklistRefreshToken
from apps.clients.validators import ClientPhoneValidator
from services.jwt_token.exceptions import (
    DecodeJWTError,
    TokenExpireError,
    TokenInBlacklistError,
)
from services.notification.base import INotificationReceiver
from services.notification.exceptions import SendSmsError


@dataclass
class AuthClientAction:
    code_service: VerificationCodeService
    token_service: BlacklistRefreshToken
    notification_service: INotificationReceiver
    validator: ClientPhoneValidator

    def login(self, phone: str, code: str) -> tuple[str, str]:
        self.validator.validate(phone)
        if self.code_service.check_code(phone, code):
            refresh = self.token_service.for_client(phone)
            access = self.token_service.access_token(refresh)
            return refresh, access

        else:
            raise InvalidCredentials()

    def send_code(self, phone: str) -> None:
        self.validator.validate(phone)
        code = self.code_service.generate_code(phone)
        try:
            self.notification_service.receive(
                {
                    "to": phone,
                    "message": f"You code {code}",
                }
            )
        except SendSmsError:
            raise SmsServiceError()

    def refresh_token(self, refresh: str) -> str:
        try:
            access = self.token_service.access_token(refresh)
        except DecodeJWTError:
            raise JWTTokenInvalid()
        except TokenExpireError:
            raise JWTTokenExpired()
        except TokenInBlacklistError:
            raise TokenInBlacklist()
        return access

    def logout(self, refresh: str) -> None:
        try:
            self.token_service.set_blacklist(refresh)
        except DecodeJWTError:
            raise JWTTokenInvalid()
        except TokenExpireError:
            raise JWTTokenExpired()
