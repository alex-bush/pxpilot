from typing import Protocol


class NotificationMessage:
    """ Represents a container for building notification messages incrementally. """

    def __init__(self):
        self._notification_message = str()

    def get(self) -> str:
        """
        Retrieve the notification message.
        :return: notification message.
        """
        return self._notification_message

    def append(self, string: str):
        """
        Append a string to the notification message.
        :param string: string to append to the notification message.
        """
        self._notification_message += string


class Notifier(Protocol):
    def create_message(self) -> NotificationMessage:
        """
        Create a new instance of a NotificationMessage.
        """
        pass

    def send(self, message: NotificationMessage):
        """
        Send a notification message.
        :param message: notification message to send.
        """
        pass
