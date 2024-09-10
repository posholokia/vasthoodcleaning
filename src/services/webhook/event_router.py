from dataclasses import dataclass
from enum import Enum
from typing import Any

from apps.clients.actions import ClientAction
from apps.jobs.actions.job import JobAction
from apps.jobs.services.parser.job import parse_job
from loguru import logger


class AllowedEvents(Enum):
    customer_create: str = "customer.created"
    customer_delete: str = "customer.deleted"
    job_created: str = "job.created"
    job_updated: str = "job.updated"


@dataclass
class WebhookEventRouter:
    """
    Класс маршрутизации событий получаемых через вебхук из CRM.
    """

    client_action: ClientAction
    job_action: JobAction

    def route_event(self, event_data: dict):
        """
        Основной метод, проверяет тип события и передает данные в action.

        :param event_data: json полученный через вебхук
        :return: None
        """
        try:
            event_type_str: str = event_data["event"]
            event_type = AllowedEvents(event_type_str)
        except ValueError:
            return  # если событие не обрабатывается, выход из функции
        except KeyError:
            logger.error("Не найден ключ 'event' в вебхуке: {}", event_data)
            return

        if event_type is AllowedEvents.customer_create:
            try:
                self.client_action.create_if_not_exists(
                    event_data["customer"]["id"],
                    event_data["customer"]["mobile_number"],
                )
            except KeyError as e:
                logger.error(
                    "Ошибка при обработке события customer.create: {}\n"
                    "data: {}",
                    e,
                    event_data,
                )

        elif event_type is AllowedEvents.customer_delete:
            try:
                self.client_action.delete_customer(
                    event_data["customer"]["id"]
                )
            except KeyError as e:
                logger.error(
                    "Ошибка при обработке события customer.delete: {}\n"
                    "data: {}",
                    e,
                    event_data,
                )

        elif event_type is AllowedEvents.job_created:
            try:
                self._job_create_handler(event_data["job"])
            except KeyError as e:
                logger.error(
                    "Ошибка при обработке события job.create: {}\ndata: {}",
                    e,
                    event_data,
                )

        elif event_type is AllowedEvents.job_updated:
            try:
                self._job_update_handler(event_data["job"])
            except KeyError as e:
                logger.error(
                    "Ошибка при обработке события job.update: {}\ndata: {}",
                    e,
                    event_data,
                )

    def _job_create_handler(self, job_data: dict[str, Any]) -> None:
        """
        Обработка события создания работы.

        :param job_data: json с данными о работе
        :return: None
        """
        customer = self.client_action.get_or_create(
            job_data["customer"]["id"],
            job_data["customer"]["mobile_number"],
        )
        job = parse_job(job_data)
        self.job_action.create(customer.id, job)

    def _job_update_handler(self, job_data: dict[str, Any]) -> None:
        """
        Обработка события обновления работы.

        :param job_data: json с данными о работе
        :return: None
        """
        job = parse_job(job_data)
        if self.job_action.exists(job.id):
            self.job_action.update(job)
        else:
            customer = self.client_action.get_or_create(
                job_data["customer"]["id"],
                job_data["customer"]["mobile_number"],
            )
            self.job_action.create(customer.id, job)
