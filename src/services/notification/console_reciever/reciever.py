import sys
from dataclasses import dataclass

from services.notification.base import INotificationReceiver


@dataclass
class ConsoleNotificationReceiver(INotificationReceiver):
    def connect(self) -> None:
        pass

    def receive(self, data: dict) -> None:
        assert data.get("to"), "Missing key 'to' in data to send"
        assert data.get("message"), "Missing key 'message' in data to send"

        sys.stderr.write(
            f"\n---------------------------SMS---------------------------\n"
            f"Notification: to {data['to']}, message: {data['message']}\n"
            f"---------------------------------------------------------\n\n"
        )
