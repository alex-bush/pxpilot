import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

from . import Notifier

logger = logging.getLogger(__name__)


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
            logger.debug(f"Send notification to {notifier}")
            try:
                notifier.send(message)
            except KeyError as ke:
                logger.error(f"Missing parameter in config for {notifier.__class__}: {ke}")
            except Exception as ex:
                logger.error(f"Error on sending using {notifier.__class__}: {ex}")

    def _build_notifiers(self, notifications_settings: Dict[str, Any]) -> List[Notifier]:
        notifiers = []
        for key, value in notifications_settings.items():
            if key in self._notifier_types:
                if not value.get("disabled", False):
                    notifiers.append(self._notifier_types[key](value))

        return notifiers
