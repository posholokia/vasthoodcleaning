from functools import lru_cache

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
from services.notification.config import BuildNotificationConfig
from services.notification.sms_receiver.conf import SMSTwilioConfig
from services.notification.sms_receiver.reciever import SMSNotificationReceiver


@lru_cache(1)
def get_container() -> Container:
    return _initialize_container()


def _initialize_container() -> Container:
    container = Container()

    def build_sms_notifications() -> SMSNotificationReceiver:
        config = BuildNotificationConfig.build_from_env(SMSTwilioConfig)
        return SMSNotificationReceiver(config=config)

    # repository
    container.register(ISiteRepository, ORMSiteRepository)

    # notification
    container.register(SMSNotificationReceiver, factory=build_sms_notifications)

    # admin perms
    container.register(AdminCanAddSitePermission)
    container.register(AdminCanDeleteSitePermission)

    # actions
    container.register(LandingAction)
    return container
