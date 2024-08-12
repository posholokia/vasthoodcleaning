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
from django.conf import settings
from punq import (
    Container,
    Scope,
)
from services.notification.base import INotificationReceiver
from services.notification.console_reciever.reciever import (
    ConsoleNotificationReceiver,
)
from services.notification.sms_receiver.reciever import SMSNotificationReceiver
from services.redis_pool.connection import RedisPool


@lru_cache(1)
def get_container() -> Container:
    return DiContainer().initialize_container()


class DiContainer:
    container = Container()

    def initialize_container(self) -> Container:
        self.__init_repository_containers()
        self.__init_service_containers()
        self.__init_permissions_containers()
        self.__init_validator_containers()
        self.__init_action_containers()

        return self.container

    def __init_repository_containers(self) -> None:
        self.container.register(RedisPool, scope=Scope.singleton)
        self.container.register(
            ICodeStorage,
            lambda: RedisCodeStorage(
                conn=self.container.resolve(
                    RedisPool, db_number=settings.CONF.redis_db_code
                )
            ),
        )
        self.container.register(
            ITokenStorage,
            lambda: RedisTokenStorage(
                conn=self.container.resolve(
                    RedisPool, db_number=settings.CONF.redis_db_token
                )
            ),
        )
        self.container.register(ISiteRepository, ORMSiteRepository)

    def __init_permissions_containers(self) -> None:
        self.container.register(AdminCanAddSitePermission)
        self.container.register(AdminCanDeleteSitePermission)

    def __init_action_containers(self) -> None:
        self.container.register(LandingAction)
        self.container.register(AuthClientAction)

    def __init_validator_containers(self) -> None:
        self.container.register(ClientPhoneValidator)

    def __init_service_containers(self) -> None:
        self.container.register(BlacklistRefreshToken)
        self.container.register(VerificationCodeService)

        if settings.CONF.environ == EnvironVariables.prod:
            self.container.register(
                INotificationReceiver,
                SMSNotificationReceiver,
            )
        elif settings.CONF.environ == EnvironVariables.local:
            self.container.register(
                INotificationReceiver,
                ConsoleNotificationReceiver,
            )
