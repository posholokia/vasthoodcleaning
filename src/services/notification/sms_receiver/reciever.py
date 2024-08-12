from dataclasses import dataclass

from django.conf import settings
from loguru import logger
from services.notification.base import INotificationReceiver
from twilio.base.exceptions import TwilioException
from twilio.rest import Client


@dataclass
class SMSNotificationReceiver(INotificationReceiver):
    async def connect(self) -> Client:
        client = Client(settings.CONF.account_sid, settings.CONF.auth_token)
        return client

    async def receive(self, data: dict) -> None:
        assert data.get("to"), "Missing key 'to' in data to send"
        assert data.get("message"), "Missing key 'message' in data to send"

        try:
            client = await self.connect()
            client.messages.create(
                to=data.get("to"),
                body=data.get("message"),
                from_=settings.CONF.from_number,
            )
        except TwilioException as e:
            logger.error("Ошибка отправки сообщения: {}", e)
