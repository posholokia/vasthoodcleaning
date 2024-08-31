from dataclasses import dataclass

from apps.clients.services.code_generator.code import VerificationCodeService
from apps.clients.services.exceptions import (
    InvalidCredentials,
    JWTTokenExpired,
    JWTTokenInvalid, TokenInBlacklist, SmsServiceError,
)
from apps.clients.services.jwt_tokens.models import BlacklistRefreshToken
from apps.clients.services.validators import ClientPhoneValidator
from services.jwt_token.exceptions import (
    DecodeJWTError,
    TokenExpireError, TokenInBlacklistError,
)
from services.notification.base import INotificationReceiver
from services.notification.exceptions import SendSmsError


@dataclass
class AuthClientAction:
    code_service: VerificationCodeService
    token_service: BlacklistRefreshToken
    notification_service: INotificationReceiver
    validator: ClientPhoneValidator

    async def login(self, phone: str, code: str) -> tuple[str, str]:
        await self.validator.validate(phone)
        if await self.code_service.check_code(phone, code):
            refresh = await self.token_service.for_client(phone)
            access = await self.token_service.access_token(refresh)
            return refresh, access

        else:
            raise InvalidCredentials()

    async def send_code(self, phone: str) -> None:
        await self.validator.validate(phone)
        code = await self.code_service.generate_code(phone)
        try:
            await self.notification_service.receive(
                {
                    "to": phone,
                    "message": f"You code {code}",
                }
            )
        except SendSmsError:
            raise SmsServiceError()

    async def refresh_token(self, refresh: str) -> str:
        try:
            access = await self.token_service.access_token(refresh)
        except DecodeJWTError:
            raise JWTTokenInvalid()
        except TokenExpireError:
            raise JWTTokenExpired()
        except TokenInBlacklistError:
            raise TokenInBlacklist()
        return access

    async def logout(self, refresh: str) -> None:
        try:
            await self.token_service.set_blacklist(refresh)
        except DecodeJWTError:
            raise JWTTokenInvalid()
        except TokenExpireError:
            raise JWTTokenExpired()
