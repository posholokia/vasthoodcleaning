from functools import lru_cache

from apps.admin_panel.permissons import AdminCanAddSitePermission
from apps.admin_panel.permissons.permissions import (
    AdminCanDeleteSitePermission,
)
from apps.clients.actions import AuthClientAction
from apps.clients.services.code_generator.code import VerificationCodeService
from apps.clients.services.code_generator.storage import (
    ICodeStorage,
    RedisCodeStorage,
)
from apps.clients.services.jwt_tokens.models import BlacklistRefreshToken
from apps.clients.services.jwt_tokens.storage.base import ITokenStorage
from apps.clients.services.jwt_tokens.storage.cache import RedisTokenStorage
from apps.clients.services.validators import ClientPhoneValidator
from apps.landing.actions.actions import LandingAction
from apps.landing.services.storage import (
    ISiteRepository,
    ORMSiteRepository,
)
from config.settings.services import EnvironVariables
from config import settings
from core.di_container import (
    Container,
    ContainerBuilder,
    TestContainer,
    Dependency as Dep,
)
from services.notification.base import INotificationReceiver
from services.notification.console_reciever.reciever import (
    ConsoleNotificationReceiver,
)
from services.notification.sms_receiver.reciever import SMSNotificationReceiver
from services.redis_pool.connection import RedisPool
from loguru import logger


@lru_cache(1)
def get_container() -> Container:
    match settings.CONF.environ:
        case EnvironVariables.local:
            logger.debug("call local container ")
            return _get_test_container()
        case EnvironVariables.prod:
            logger.debug("call prod container ")
            return _get_main_container()
    raise Exception("Для этого типа окружения не установлен контейнер")


def _get_main_container() -> Container:
    return DiContainer().initialize_container()


def _get_test_container():
    container = _get_main_container().create_test_container()
    return DiTestContainer(container).initialize_container()


class DiContainer:
    builder = ContainerBuilder()

    def initialize_container(self) -> Container:
        self.__init_redis_containers()
        self.__init_repository_containers()
        self.__init_service_containers()
        self.__init_permissions_containers()
        self.__init_validator_containers()
        self.__init_action_containers()

        self.container = self.builder.build()
        return self.container

    def __init_redis_containers(self) -> None:
        self.builder.register(
            "RedisCode", RedisPool, db_number=settings.CONF.redis_db_code,
        )
        self.builder.register(
            "RedisToken", RedisPool, db_number=settings.CONF.redis_db_token,
        )
        self.builder.register(
            ICodeStorage,
            RedisCodeStorage,
            conn=Dep("RedisCode")
        )
        self.builder.register(
            ITokenStorage,
            RedisTokenStorage,
            conn=Dep("RedisToken")
        )

    def __init_repository_containers(self) -> None:
        self.builder.register(ISiteRepository, ORMSiteRepository)

    def __init_permissions_containers(self) -> None:
        self.builder.register(
            AdminCanAddSitePermission, AdminCanAddSitePermission,
        )
        self.builder.register(
            AdminCanDeleteSitePermission, AdminCanDeleteSitePermission,
        )

    def __init_action_containers(self) -> None:
        self.builder.register(LandingAction, LandingAction)
        self.builder.register(AuthClientAction, AuthClientAction)

    def __init_validator_containers(self) -> None:
        self.builder.register(ClientPhoneValidator, ClientPhoneValidator)

    def __init_service_containers(self) -> None:
        self.builder.register(BlacklistRefreshToken, BlacklistRefreshToken)
        self.builder.register(VerificationCodeService, VerificationCodeService)
        self.builder.register(
            INotificationReceiver,
            SMSNotificationReceiver,
        )


class DiTestContainer:
    def __init__(self, container: TestContainer):
        self.container = container

    def initialize_container(self) -> TestContainer:
        self.container = self.container.with_overridden(
            INotificationReceiver,
            ConsoleNotificationReceiver,
        )
        return self.container
