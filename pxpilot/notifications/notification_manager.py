from datetime import datetime, timedelta

from . import Notifier
from .log import LOGGER
from .notifier_types import notifier_types


class NotificationManager:
    def __init__(self, config):
        self._status_count = 0
        self._notifiers = [notifier for notifier in (self._create_notifier(n) for n in config) if notifier is not None]
        self._message_notifier_map = {n.create_message(): n for n in self._notifiers}

    def start(self, start_time: datetime):
        for message in self._message_notifier_map.keys():
            message.add_header(start_time)

    def append_status(self, vm_type, vm_id, vm_name, vm_status, start_time, duration: timedelta):
        for message in self._message_notifier_map.keys():
            message.append_vm_status(vm_type, vm_id, vm_name, vm_status, start_time, duration)

    def append_error(self, error_message: str) -> None:
        for message in self._message_notifier_map.keys():
            message.append_error(error_message)

    def fatal(self, error_message: str) -> None:
        for message in self._message_notifier_map.keys():
            message.fatal(error_message)

    def send(self):
        for message, notifier in self._message_notifier_map.items():
            LOGGER.debug(f"Send notification to {notifier}")
            notifier.send(message)

    @staticmethod
    def _create_notifier(notifier_config) -> Notifier:
        for key in notifier_config.keys():
            if key in notifier_types:
                LOGGER.debug(f"Creating '{key}' notifier.")
                return notifier_types[key](notifier_config[key])
