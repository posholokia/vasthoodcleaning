import re
from dataclasses import dataclass

from apps.clients.exceptions import PhoneFormatError

from core.constructor.validators import BaseValidator


@dataclass
class ClientPhoneValidator(BaseValidator):
    """
    Валидация номера телефона клиента
    """

    def validate(self, phone: str) -> None:
        pattern = re.compile(r"^\+\d{10,15}$")

        if not re.match(pattern, phone):
            raise PhoneFormatError()
