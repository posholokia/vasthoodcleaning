from dataclasses import dataclass

from twilio.rest import Client

from services.notification.base import INotificationReceiver
from django.conf import settings


@dataclass
class SMSNotificationReceiver(INotificationReceiver):
    async def connect(self) -> Client:
        client = Client(
            settings.conf.account_sid,
            settings.conf.auth_token
        )
        return client

    async def receive(self, data: dict) -> None:
        assert data.get("to"), "Missing key 'to' in data to send"
        assert data.get("message"), "Missing key 'message' in data to send"
        assert data.get("from"), "Missing key 'from' in data to send"

        client = await self.connect()
        client.messages.create(
            to=data.get("to"),
            body=data.get("message"),
            from_=data.get("from"),
        )
