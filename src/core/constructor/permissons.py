from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class BasePermission:
    def has_permission(self, *args, **kwargs) -> None: ...
