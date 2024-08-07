from functools import lru_cache

from django.conf import settings
from punq import Container

from apps.admin_panel.permissons import AdminCanAddSitePermission
from apps.admin_panel.permissons.permissions import (
    AdminCanDeleteSitePermission,
)
from apps.landing.actions.actions import LandingAction
from apps.landing.services.storage import (
    ISiteRepository,
    ORMSiteRepository,
)
from services.notification.base import INotificationReceiver
from services.notification.console_reciever.reciever import ConsoleNotificationReceiver
from services.notification.sms_receiver.reciever import SMSNotificationReceiver


@lru_cache(1)
def get_container() -> Container:
    return ContainerFactory().initialize_container()


class ContainerFactory:
    container = Container()

    def initialize_container(self) -> Container:
        self.__init_common_containers()

        if settings.ENVIRON == "prod":
            self.__init_prod_container()
        elif settings.ENVIRON == "local":
            self.__init_local_container()

        return self.container

    def __init_common_containers(self) -> None:
        # repository
        self.container.register(ISiteRepository, ORMSiteRepository)

        # admin perms
        self.container.register(AdminCanAddSitePermission)
        self.container.register(AdminCanDeleteSitePermission)

        # actions
        self.container.register(LandingAction)

    def __init_prod_container(self) -> None:
        self.container.register(INotificationReceiver, SMSNotificationReceiver)

    def __init_local_container(self) -> None:
        self.container.register(INotificationReceiver, ConsoleNotificationReceiver)
