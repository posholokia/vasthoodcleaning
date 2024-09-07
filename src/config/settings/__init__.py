from ..config_builder import ConfigBuilder
from .common import *
from .database import *
from .house_pro import HouseProConf
from .logger import logger  # noqa
from .redis import RedisConf
from .services import ServiceConf
from .twilio_config import SMSTwilioConfig


class Configs(
    SMSTwilioConfig,
    RedisConf,
    ServiceConf,
    HouseProConf,
):
    pass


conf = ConfigBuilder.build_from_env(Configs)
