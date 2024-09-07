from dataclasses import dataclass

from apps.landing.models import Site
from apps.landing.storage import ISiteRepository

from core.constructor.permissons import BasePermission


@dataclass(frozen=True, eq=False)
class AdminCanAddSitePermission(BasePermission):
    repository: ISiteRepository

    def has_permission(self) -> bool:
        if Site.objects.exists():
            return False
        return True


@dataclass(frozen=True, eq=False)
class AdminCanDeleteSitePermission(BasePermission):
    repository: ISiteRepository

    def has_permission(self) -> bool:
        if Site.objects.exists():
            return False
        return True
