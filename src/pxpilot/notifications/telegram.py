import logging
import re

import requests

from .notifications import NotificationMessage, Notifier, ProxmoxMessage

logger = logging.getLogger(__name__)


class TelegramMessage(ProxmoxMessage):
    pass


class TelegramNotifier(Notifier):
    """ Implements the Notifier protocol to send notifications via Telegram. """

    def __init__(self, config):
        self._config = config

    def create_message(self) -> NotificationMessage:
        return TelegramMessage()

    def send(self, notification_message: NotificationMessage):

        base_url = "https://api.telegram.org/bot"
        send_url = f"{self._config['token']}/sendMessage?chat_id"
        parse_url = f"parse_mode={notification_message.mode}"

        url = f"{base_url}{send_url}={self._config['chat_id']}&{parse_url}"

        if notification_message.mode == "HTML":
            msg = notification_message.message
        else:
            msg = self._escape(notification_message.message)

        response = requests.post(url, json={'text': msg}, timeout=10)

        match response.status_code:
            case 200:
                logger.info("Notification has been send successfully.")
            case 400:
                logger.warning("Bad request. " + response.text)
            case 401:
                logger.warning("Cannot access to noti")

    @staticmethod
    def _escape(text):
        """
        Escape special characters in the text to conform to Telegram Markdown V2.
        """
        special_chars = "[]()~`>#+-=|{}.!"
        pattern = re.compile(r'([' + re.escape(special_chars) + '])')
        return pattern.sub(r'\\\1', text)
