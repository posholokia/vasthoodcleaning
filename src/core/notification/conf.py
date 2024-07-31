from abc import ABC
from pydantic import BaseConfig


class NotificationConfig(ABC, BaseConfig):
    @classmethod
    def build_from_env(cls) -> dict:
        raise NotImplementedError
