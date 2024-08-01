from dataclasses import dataclass
from twilio.rest import Client
from pydantic_settings import BaseSettings

from services.notification.base import INotificationReceiver


@dataclass
class SMSNotificationReceiver(INotificationReceiver):
    config: BaseSettings

    async def connect(self) -> Client:
        client = Client(
            self.config.account_sid,
            self.config.auth_token
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


if __name__ == "__main__":
    import asyncio
    from config.containers import get_container

    async def main():
        container = get_container()
        sms: SMSNotificationReceiver = container.resolve(SMSNotificationReceiver)
        data = {
            "to": "+13126848315",
            "message": "test sms service",
            "from": "+17639103848",
        }
        await sms.receive(data)

    asyncio.run(main())
