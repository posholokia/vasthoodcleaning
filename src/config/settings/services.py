from enum import Enum

from pydantic_settings import BaseSettings


class EnvironVariables(Enum):
    prod: str = "prod"
    local: str = "local"
    test: str = "test"


class ServiceConf(BaseSettings):
    crypto_key: str
    environ: EnvironVariables
