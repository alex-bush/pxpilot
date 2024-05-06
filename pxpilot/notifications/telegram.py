import re

import requests

from .log import LOGGER
from .notifications import NotificationMessage, Notifier


class TelegramMessage(NotificationMessage):
    pass


class TelegramNotifier(Notifier):
    """ Implements the Notifier protocol to send notifications via Telegram. """

    def __init__(self, config):
        self._config = config

    def create_message(self) -> NotificationMessage:
        return TelegramMessage()

    def send(self, notification_message: NotificationMessage):
        url = f"https://api.telegram.org/bot{self._config['token']}/sendMessage?chat_id={self._config['chat_id']}&parse_mode=MarkdownV2"

        msg = self._escape(notification_message.get())

        response = requests.post(url, json={'text': msg}, timeout=10)

        match response.status_code:
            case 200:
                LOGGER.info("Notification has been send successfully.")
            case 400:
                LOGGER.warning("Bad request. " + response.text)
            case 401:
                LOGGER.warning("Cannot access to noti")

    @staticmethod
    def _escape(text):
        """
        Escape special characters in the text to conform to Telegram Markdown V2.
        """
        special_chars = "[]()~`>#+-=|{}.!"
        pattern = re.compile(r'([' + re.escape(special_chars) + '])')
        return pattern.sub(r'\\\1', text)
