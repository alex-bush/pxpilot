from datetime import datetime, timedelta
from typing import List

from . import Notifier
from .log import LOGGER


class NotificationManager:
    def __init__(self, config, notifier_types):
        self._status_count = 0
        self._notifier_types = notifier_types

        self._notifiers = self._build_notifiers(config)
        self._message_to_notifier_map = {n.create_message(): n for n in self._notifiers}

    def start(self, start_time: datetime):
        for message in self._message_to_notifier_map.keys():
            message.add_header(start_time)

    def append_status(self, vm_type, vm_id, vm_name, vm_status, start_time, duration: timedelta):
        for message in self._message_to_notifier_map.keys():
            message.append_vm_status(vm_type, vm_id, vm_name, vm_status, start_time, duration)

    def append_error(self, error_message: str) -> None:
        for message in self._message_to_notifier_map.keys():
            message.append_error(error_message)

    def fatal(self, error_message: str) -> None:
        for message in self._message_to_notifier_map.keys():
            message.fatal(error_message)

    def send(self):
        for message, notifier in self._message_to_notifier_map.items():
            LOGGER.debug(f"Send notification to {notifier}")
            try:
                notifier.send(message)
            except KeyError as ke:
                LOGGER.error(f"Missing parameter in config for {notifier.__class__}: {ke}")
            except Exception as ex:
                LOGGER.error(f"Error on sending using {notifier.__class__}: {ex}")

    def _build_notifiers(self, config) -> List[Notifier]:
        return [notifier for notifier in
                (self._create_notifier(n) for n in config)
                if notifier is not None]

    def _create_notifier(self, notifier_config) -> Notifier | None:
        for key in notifier_config.keys():
            if key in self._notifier_types:
                LOGGER.debug(f"Creating '{key}' notifier.")
                config = notifier_config[key]
                if not notifier_config[key].get("disabled", False):
                    return self._notifier_types[key](config)
        return None
