from dataclasses import dataclass

from django.conf import settings
from loguru import logger
from services.notification.base import INotificationReceiver
from services.notification.exceptions import SendSmsError
from twilio.base.exceptions import TwilioException
from twilio.rest import Client


@dataclass
class SMSNotificationReceiver(INotificationReceiver):
    """
    Отправка уведомлений по СМС.
    """

    def __init__(self):
        client = Client(settings.conf.account_sid, settings.conf.auth_token)
        self.client = client

    def send(self, to_: str, message: str) -> None:
        try:
            self.client.messages.create(
                to=to_,
                body=message,
                from_=settings.conf.from_number,
            )
        except TwilioException as e:
            logger.error("Ошибка отправки сообщения: {}", e)
            raise SendSmsError(e)
