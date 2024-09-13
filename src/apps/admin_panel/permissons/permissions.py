from dataclasses import dataclass

from apps.landing.models import Site

from core.constructor.permissons import BasePermission


@dataclass(frozen=True, eq=False)
class AdminCanAddSitePermission(BasePermission):
    def has_permission(self) -> bool:
        if Site.objects.exists():
            return False
        return True


@dataclass(frozen=True, eq=False)
class AdminCanDeleteSitePermission(BasePermission):
    def has_permission(self) -> bool:
        if Site.objects.exists():
            return False
        return True
