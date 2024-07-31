import re

from apps.accounts.services.exceptions.user import InvalidProneNumber
from core.constructor.validators import BaseValidator


class UserValidator(BaseValidator):
    @classmethod
    def validate(cls, *args, **kwargs) -> None:
        if phone := kwargs.get("phone"):
            cls._phone_validator(phone)

    @classmethod
    def _phone_validator(cls, phone: str) -> None:
        pattern = re.compile(r"^\+\d{10,15}$")
        if pattern.match(phone) is None:
            raise InvalidProneNumber(message=f"Invalid phone number: {phone}")
