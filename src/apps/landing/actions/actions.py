from dataclasses import dataclass

from apps.landing.models import (
    ServiceDetailEntity,
    SiteEntity,
)
from apps.landing.storage import ISiteRepository


@dataclass
class LandingAction:
    storage: ISiteRepository

    def get_site(self) -> SiteEntity:
        """
        Получить всю страницу сайта. Страница может быть только одна.

        :return: Сайт.
        """
        return self.storage.get()

    def get_service(self, service_pk: int) -> ServiceDetailEntity:
        """
        Получить подробную информацию об услуге.

        :param service_pk:  ID Услуги.
        :return:            Услуга с детальной информацией.
        """
        return self.storage.get_service_detail(service_pk)
