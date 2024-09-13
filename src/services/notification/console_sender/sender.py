import sys
from dataclasses import dataclass

from services.notification.base import INotificationReceiver


@dataclass
class ConsoleNotificationReceiver(INotificationReceiver):
    def send(self, to_: str, message: str) -> None:
        sys.stderr.write(
            f"\n---------------------------SMS---------------------------\n"
            f"Notification: to {to_}, message: {message}\n"
            f"---------------------------------------------------------\n\n"
        )
