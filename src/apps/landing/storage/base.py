from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from apps.landing.models import (
    ServiceDetailEntity,
    SiteEntity,
)


@dataclass
class ISiteRepository(ABC):
    @abstractmethod
    def get(self) -> SiteEntity:
        """
        Возвращает страницу сайта со всем содержимым.

        :return: Сайт.
        """

    @abstractmethod
    def get_service_detail(self, service_pk: int) -> ServiceDetailEntity:
        """
        Возвращает подробное описание услуги.

        :param service_pk:  ID услуги.
        :return:            Сайт.
        """
