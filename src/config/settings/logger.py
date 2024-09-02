from loguru import logger
from .common import BASE_DIR


LOG_DIR = BASE_DIR / "logs"


logger.add(
    LOG_DIR / 'debug.log',
    level='DEBUG',
    rotation='1 MB',
    retention='30 days',
    format="{time} {level} {message}",
    enqueue=True,
    diagnose=False,
    backtrace=False,
)
logger.add(
    LOG_DIR / 'warnings.log',
    level='WARNING',
    rotation='1 MB',
    retention='30 days',
    format="{time} {level} {message}",
    enqueue=True,
    diagnose=False,
    backtrace=False,
)
logger.add(
    LOG_DIR / 'errors.log',
    level='ERROR',
    rotation='1 MB',
    retention='30 days',
    format="{time} {level} {message}",
    enqueue=True,
    diagnose=False,
    backtrace=False,
)
