import time
import random
from dataclasses import (
    dataclass,
    field,
)

from apps.clients.services.code_generator.exceptions import (
    TooOftenSendingError,
)
from apps.clients.services.code_generator.storage import ICodeStorage
from config.settings import conf
from config.settings.services import EnvironVariables


@dataclass
class VerificationCodeService:
    """
    Сервис генерации и проверки одноразового кода для аутентификации.
    """

    storage: ICodeStorage
    code_interval: int = field(  # допустимый интервал между смс
        init=False, default=60
    )

    def generate_code(self, phone: str) -> str:
        """
        Генератор одноразового кода.

        :param phone:   Номер телефона клиента.
        :return:        Одноразовый код.
        """
        if conf.environ == EnvironVariables.prod:
            digest = "0123456789"
        else:
            digest = "1"  # не для прода код всегда 111111

        code = "".join(random.choices(digest, k=6))  # код из 6 цифр
        created_at = time.time()

        if code_with_exp := self.storage.get_code(phone):
            code, exp = code_with_exp.split("-")

            # проверяем, что между отправками кода прошло более 60 секунд
            if created_at - float(exp) < self.code_interval:
                raise TooOftenSendingError()

        self.storage.save_code(phone, f"{code}-{created_at}")
        return code

    def check_code(self, phone: str, user_code: str) -> bool:
        """
        Проверка корректности введенного клиентом кода.

        :param phone:       Номер телефона клиента.
        :param user_code:   Шестизначный код, который ввел клиент.
        :return:            Bool.
        """
        code_with_exp = self.storage.get_code(phone)

        if code_with_exp is None:
            return False

        code, _ = code_with_exp.split("-")

        if code == user_code:
            # удаляем код в случае успешной проверки
            self.storage.delete_code(phone)
            return True

        return False
