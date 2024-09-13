from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class BasePermission:
    """
    Базовый конструктор проверки прав.
    """

    def has_permission(self, *args, **kwargs) -> None:
        """
        Основной метод проверки прав.

        :param args: в зависимости от конкретной реализации
        :param kwargs: в зависимости от конкретной реализации
        :return None: поднимает ошибку, если проверка прав не пройдена.
        """
