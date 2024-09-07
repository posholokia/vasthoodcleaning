from dataclasses import dataclass
from enum import Enum

from apps.clients.actions import ClientAction
from apps.jobs.actions.job import JobAction
from loguru import logger


class AllowedEvents(Enum):
    customer_create: str = "customer.created"
    customer_delete: str = "customer.deleted"
    job_created: str = "job.created"
    job_updated: str = "job.updated"


@dataclass
class WebhookEventRouter:
    __client_action: ClientAction
    __job_action: JobAction

    def route_event(self, event_data: dict):
        try:
            event_type_str = event_data["event"]
            event_type = AllowedEvents(event_type_str)
        except AttributeError:
            return
        except KeyError:
            logger.error(
                "Не найден ключ 'event' в вебхуке: {}",
                event_data
            )
            return

        if event_type is AllowedEvents.customer_create:
            try:
                customer = event_data["customer"]
                self.__client_action.create_if_not_exists(customer)
            except KeyError:
                logger.error(
                    "В событии customer.create е найден ключ 'customer': {}",
                    event_data
                )

        elif event_type is AllowedEvents.customer_delete:
            try:
                customer = event_data["customer"]
                self.__client_action.delete_customer(customer)
            except KeyError:
                logger.error(
                    "В событии customer.delete е найден ключ 'customer': {}",
                    event_data
                )

        elif event_type is AllowedEvents.job_created:
            try:
                customer_data = event_data["job"]["customer"]
                self.__client_action.create_if_not_exists(customer_data)
                self.__job_action.create(event_data["job"])
            except KeyError:
                logger.error(
                    "В событии job.create е найден ключ "
                    "'job' или 'customer': {}",
                    event_data,
                )
        elif event_type is AllowedEvents.job_updated:
            if self.__job_action.exists(event_data["job"]["id"]):
                self.__job_action.update(event_data["job"])
            else:
                customer_data = event_data["job"]["customer"]
                self.__client_action.create_if_not_exists(customer_data)
                self.__job_action.create(event_data["job"])


if __name__ == '__main__':

    r = WebhookEventRouter()
    r.route_event({"event": "customer.created"})
