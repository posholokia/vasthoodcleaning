from ..config_builder import ConfigBuilder
from .common import *
from .database import *
from .twilio_config import SMSTwilioConfig


class Configs(SMSTwilioConfig):
    pass


conf = ConfigBuilder.build_from_env(Configs)
