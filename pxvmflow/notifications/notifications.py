from typing import Protocol


class NotificationMessage(Protocol):
    def get(self) -> str:
        pass

    def append(self, string: str):
        pass


class Notifier(Protocol):
    def get_message(self) -> NotificationMessage:
        pass

    def send(self, message: NotificationMessage):
        pass
