from dataclasses import dataclass

from apps.landing.models import Site
from apps.landing.services.storage import ISiteRepository
from services.constructor.permissons import BasePermission


@dataclass(frozen=True, eq=False)
class AdminCanAddSitePermission(BasePermission):
    repository: ISiteRepository

    async def has_permission(self) -> bool:
        if await Site.objects.aexists():
            return False
        return True


@dataclass(frozen=True, eq=False)
class AdminCanDeleteSitePermission(BasePermission):
    repository: ISiteRepository

    async def has_permission(self) -> bool:
        if await Site.objects.aexists():
            return False
        return True
