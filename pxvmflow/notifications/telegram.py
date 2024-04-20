import re

import requests

from .log import LOGGER
from .notifications import NotificationMessage, Notifier


class TelegramMessage(NotificationMessage):
    def __init__(self):
        self._message = str()

    def get(self) -> str:
        return self._message

    def append(self, string: str):
        self._message += string


class TelegramNotifier(Notifier):
    def __init__(self, config):
        self._config = config

    def get_message(self) -> NotificationMessage:
        return TelegramMessage()

    def escape(self, text):
        special_chars = "[]()~`>#+-=|{}.!"
        pattern = re.compile(r'([' + re.escape(special_chars) + '])')
        return pattern.sub(r'\\\1', text)

    def send(self, message: NotificationMessage):
        url = f'https://api.telegram.org/bot{self._config['token']}/sendMessage?chat_id={self._config['chat_id']}&parse_mode=MarkdownV2'

        msg = self.escape(message.get())

        response = requests.post(url, json={'text': msg}, timeout=10)

        match response.status_code:
            case 200:
                LOGGER.info("Notification has been send successfully.")
            case 400:
                LOGGER.warn("Bad request. " + response.text)
            case 401:
                LOGGER.warn("Cannot access to noti")
