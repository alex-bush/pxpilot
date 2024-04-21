from typing import Protocol


class NotificationMessage:
    def __init__(self):
        self._notification_message = str()

    def get(self) -> str:
        return self._notification_message

    def append(self, string: str):
        self._notification_message += string


class Notifier(Protocol):
    def get_message(self) -> NotificationMessage:
        pass

    def send(self, message: NotificationMessage):
        pass
