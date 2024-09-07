from functools import lru_cache

from apps.admin_panel.permissons import AdminCanAddSitePermission
from apps.admin_panel.permissons.permissions import (
    AdminCanDeleteSitePermission,
)
from apps.clients.actions import (
    AuthClientAction,
    ClientAction,
)
from apps.clients.services.code_generator.code import VerificationCodeService
from apps.clients.services.code_generator.storage import (
    ICodeStorage,
    RedisCodeStorage,
)
from apps.clients.services.jwt_tokens.models import BlacklistRefreshToken
from apps.clients.services.jwt_tokens.storage.base import ITokenStorage
from apps.clients.services.jwt_tokens.storage.cache import RedisTokenStorage
from apps.clients.storage.base import IClientRepository
from apps.clients.storage.orm import ORMClientRepository
from apps.clients.validators import ClientPhoneValidator
from apps.jobs.actions.job import JobAction
from apps.jobs.services.parser import JobDetailJsonParser
from apps.jobs.storage.base import IJobRepository
from apps.jobs.storage.orm import ORMJobRepository
from apps.landing.actions.actions import LandingAction
from apps.landing.storage import (
    ISiteRepository,
    ORMSiteRepository,
)
from config import settings
from config.settings.services import EnvironVariables
from ninja.security import APIKeyHeader
from services.crm.base import ICRM
from services.crm.house_pro.interface import HouseProCRM
from services.notification.base import INotificationReceiver
from services.notification.console_reciever.reciever import (
    ConsoleNotificationReceiver,
)
from services.notification.sms_receiver.reciever import SMSNotificationReceiver
from services.redis_pool.connection import RedisPool
from services.webhook.event_router import WebhookEventRouter

from core.containers.di_container import (
    Container,
    ContainerBuilder,
    Dependency as Dep,
    TestContainer,
)
from core.security.auth.webhook import (
    ApiKey,
    ApiKeyLocal,
)


@lru_cache(1)
def get_container() -> Container:
    match settings.conf.environ:
        case EnvironVariables.local:
            return _get_local_container()
        case EnvironVariables.prod:
            return _get_main_container()
        case EnvironVariables.test:
            return _get_test_container()
    raise Exception("Для этого типа окружения не установлен контейнер")


def _get_main_container() -> Container:
    return DiContainer().initialize_container()


def _get_test_container():
    container = _get_main_container().create_test_container()
    return DiTestContainer(container).initialize_container()


def _get_local_container():
    container = _get_main_container().create_test_container()
    return DiLocalContainer(container).initialize_container()


class DiContainer:
    builder = ContainerBuilder()

    def initialize_container(self) -> Container:
        self.__init_redis_containers()
        self.__init_repository_containers()
        self.__init_service_containers()
        self.__init_permissions_containers()
        self.__init_validator_containers()
        self.__init_action_containers()
        self.__init_webhook_container()
        self.container = self.builder.build()
        return self.container

    def __init_redis_containers(self) -> None:
        self.builder.register(
            "RedisCode",
            RedisPool,
            db_number=settings.conf.redis_db_code,
        )
        self.builder.register(
            "RedisToken",
            RedisPool,
            db_number=settings.conf.redis_db_token,
        )
        self.builder.register(
            "RedisCache",
            RedisPool,
            db_number=settings.conf.redis_db_cache,
        )
        self.builder.register(
            ICodeStorage, RedisCodeStorage, conn=Dep("RedisCode")
        )
        self.builder.register(
            ITokenStorage, RedisTokenStorage, conn=Dep("RedisToken")
        )

    def __init_repository_containers(self) -> None:
        self.builder.register(ISiteRepository, ORMSiteRepository)
        self.builder.register(IClientRepository, ORMClientRepository)
        self.builder.register(IJobRepository, ORMJobRepository)

    def __init_permissions_containers(self) -> None:
        self.builder.register(
            AdminCanAddSitePermission,
            AdminCanAddSitePermission,
        )
        self.builder.register(
            AdminCanDeleteSitePermission,
            AdminCanDeleteSitePermission,
        )

    def __init_action_containers(self) -> None:
        self.builder.register(LandingAction, LandingAction)
        self.builder.register(AuthClientAction, AuthClientAction)
        self.builder.register(ClientAction, ClientAction)
        self.builder.register(JobAction, JobAction)

    def __init_validator_containers(self) -> None:
        self.builder.register(ClientPhoneValidator, ClientPhoneValidator)

    def __init_service_containers(self) -> None:
        self.builder.register(BlacklistRefreshToken, BlacklistRefreshToken)
        self.builder.register(VerificationCodeService, VerificationCodeService)
        self.builder.register(
            INotificationReceiver,
            SMSNotificationReceiver,
        )
        self.builder.register(APIKeyHeader, ApiKey)
        self.builder.register(ICRM, HouseProCRM)
        self.builder.register(JobDetailJsonParser, JobDetailJsonParser)

    def __init_webhook_container(self) -> None:
        self.builder.register(WebhookEventRouter, WebhookEventRouter)


class DiTestContainer:
    def __init__(self, container: TestContainer):
        self.container = container

    def initialize_container(self) -> TestContainer:
        self.container = self.container.with_overridden(
            INotificationReceiver,
            ConsoleNotificationReceiver,
        )
        return self.container


class DiLocalContainer:
    def __init__(self, container: TestContainer):
        self.container = container

    def initialize_container(self) -> TestContainer:
        self.container = self.container.with_overridden(
            INotificationReceiver,
            ConsoleNotificationReceiver,
        )
        self.container = self.container.with_overridden(
            APIKeyHeader, ApiKeyLocal
        )
        return self.container
