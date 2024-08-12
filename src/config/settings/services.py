from pydantic_settings import BaseSettings

from enum import Enum


class EnvironVariables(Enum):
    prod: str = "prod"
    local: str = "local"


class ServiceConf(BaseSettings):
    crypto_key: str
    environ: EnvironVariables
