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


@lru_cache(1)
def get_container() -> Container:
    return _initialize_container()


def _initialize_container() -> Container:
    container = Container()

    # repository
    container.register(ISiteRepository, ORMSiteRepository)

    # admin perms
    container.register(AdminCanAddSitePermission)
    container.register(AdminCanDeleteSitePermission)

    # actions
    container.register(LandingAction)
    return container
