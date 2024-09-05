from dataclasses import dataclass

from apps.landing.models import Site
from apps.landing.storage import ISiteRepository

from core.constructor.permissons import BasePermission


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
