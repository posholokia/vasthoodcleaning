from ..config_builder import ConfigBuilder
from .common import *
from .database import *
from .redis import RedisConf
from .services import ServiceConf
from .twilio_config import SMSTwilioConfig


class Configs(
    SMSTwilioConfig,
    RedisConf,
    ServiceConf,
):
    pass


CONF = ConfigBuilder.build_from_env(Configs)
