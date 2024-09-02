from ..config_builder import ConfigBuilder
from .common import *
from .database import *
from .redis import RedisConf
from .services import ServiceConf
from .twilio_config import SMSTwilioConfig
from .logger import logger  # noqa
from .house_pro import HouseProConf


class Configs(
    SMSTwilioConfig,
    RedisConf,
    ServiceConf,
    HouseProConf,
):
    pass


conf = ConfigBuilder.build_from_env(Configs)
