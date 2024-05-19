from .log import LOGGER
from .notifications import NotificationMessage, Notifier


class EmailMessage(NotificationMessage):
    pass


class EmailNotifier(Notifier):
    def __init__(self, config):
        self._config = config

    def create_message(self) -> NotificationMessage:
        return EmailMessage()

    def send(self, message: NotificationMessage):
        LOGGER.info("Email has been send successfully.")
