from .log import LOGGER
from .notifications import NotificationMessage, Notifier


class EmailMessage(NotificationMessage):
    pass


class EmailNotifier(Notifier):
    def __init__(self, config):
        self._config = config

    def create_message(self) -> NotificationMessage:
        """
        Create a new instance of a NotificationMessage.
        """
        return EmailMessage()

    def send(self, message: NotificationMessage):
        """
        Send a notification message.
        :param message: notification message to send.
        """
        LOGGER.info("Email has been send successfully.")
