import os
from typing import Type
from typing import TypeVar
from dotenv import load_dotenv


load_dotenv()

TConf = TypeVar("TConf")


class ConfigBuilder:
    @classmethod
    def build_from_env(cls, config: Type[TConf]) -> TConf:
        attrs = {}
        for field, value in config.__fields__.items():
            print()
            print(field, field.upper(), os.getenv(field.upper()))
            print()
            # преимущество над значением в init над env.
            # если в init есть значение по умолчанию, значит оно не обязательно
            # и мы записываем в конфиг значение по умолчанию, иначе ищем в env
            if not value.is_required():
                attrs.update({field: value.default})
            else:
                attrs.update({field: os.getenv(field.upper())})
        return config(**attrs)
