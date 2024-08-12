import sys
from dataclasses import dataclass

from services.notification.base import INotificationReceiver


@dataclass
class ConsoleNotificationReceiver(INotificationReceiver):
    async def connect(self) -> None:
        pass

    async def receive(self, data: dict) -> None:
        assert data.get("to"), "Missing key 'to' in data to send"
        assert data.get("message"), "Missing key 'message' in data to send"

        sys.stderr.write(
            f"Notification: to {data['to']}, message: {data['message']}"
        )
