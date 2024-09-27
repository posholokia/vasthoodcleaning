from dataclasses import dataclass

from config.settings import conf
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
        client = Client(conf.account_sid, conf.auth_token)
        self.client = client

    def send(self, to_: str, message: str) -> None:
        try:
            self.client.messages.create(
                to=to_,
                body=message,
                from_=conf.from_number,
                messaging_service_sid=conf.messaging_service_sid,
            )
        except TwilioException as e:
            logger.error("Ошибка отправки сообщения: {}", e)
            raise SendSmsError(e)


if __name__ == "__main__":
    sms = SMSNotificationReceiver()
    sms.send(
        to_="+18722587942",
        message="Your Vast Cleaning verification code is: 123456",
    )
