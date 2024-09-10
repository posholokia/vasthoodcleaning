from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseValidator(ABC):
    """
    Базовый конструктор валидаторов.
    """

    @abstractmethod
    def validate(self, *args, **kwargs) -> None:
        """
        Метод валидации аргументов.

        :param args: в зависимости от конкретной реализации
        :param kwargs: в зависимости от конкретной реализации
        :return: None, поднимает ошибку, если валидация не пройдена.
        """
