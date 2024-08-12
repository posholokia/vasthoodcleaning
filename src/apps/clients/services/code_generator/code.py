import time
import random
from dataclasses import dataclass

from apps.clients.services.code_generator.exceptions import (
    TooOftenSendingError,
)
from apps.clients.services.code_generator.storage import ICodeStorage
from config.settings.services import EnvironVariables
from django.conf import settings


@dataclass
class VerificationCodeService:
    storage: ICodeStorage
    code_interval: int = 60  # допустимый интервал между смс

    async def generate_code(self, phone: str) -> None:
        if settings.CONF.environ == EnvironVariables.prod:
            digest = "0123456789"
        else:
            digest = "1"  # не для прода код всегда 111111

        code = "".join(random.choices(digest, k=6))  # код из 6 цифр
        created_at = time.time()

        if code_with_exp := await self.storage.get_code(phone):
            code, exp = code_with_exp.split("-")

            # проверяем, что между отправками кода прошло более 60 секунд
            if created_at - float(exp) < self.code_interval:
                raise TooOftenSendingError()

        await self.storage.save_code(phone, f"{code}-{created_at}")

    async def check_code(self, phone: str, user_code: str) -> bool:
        code_with_exp = await self.storage.get_code(phone)

        if code_with_exp is None:
            return False

        code, _ = code_with_exp.split("-")

        if code == user_code:
            # удаляем код в случае успешной проверки
            await self.storage.delete_code(phone)
            return True

        return False
