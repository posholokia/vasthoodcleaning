import os
from typing import Type
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class BuildNotificationConfig:
    @classmethod
    def build_from_env(cls, config: Type[BaseSettings]) -> BaseSettings:
        attrs = {}
        for field in config.__annotations__.keys():
            attrs.update({field: os.getenv(field.upper())})
        return config(**attrs)


if __name__ == "__main__":
    from services.notification.sms_receiver.conf import SMSTwilioConfig

    c = BuildNotificationConfig.build_from_env(SMSTwilioConfig)
    print(c)
