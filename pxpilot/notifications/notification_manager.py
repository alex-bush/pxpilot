from datetime import datetime, timedelta

from . import Notifier
from .consts import *
from .log import LOGGER
from .notifier_types import notifier_types


class NotificationManager:
    def __init__(self, config):
        self._status_count = 0
        self._notifiers = [self._create_notifier(n) for n in config]
        self._message_notifier_map = {n.get_message(): n for n in self._notifiers}

    def start(self, node_name, start_time: datetime):
        for message in self._message_notifier_map.keys():
            msg = f"{ROCKET_SYMBOL} [{node_name}] *Proxmox VMs Startup Summary* _{start_time.strftime('%d-%b-%Y %H:%M:%S')}_\n\n"
            message.append(msg)

    def append_status(self, vm_type, vm_id, vm_name, vm_status, start_time, duration: timedelta):

        status_icon = CHECK_MARK_SYMBOL
        duration_str = f"{duration.seconds} seconds"
        status_str = "Successfully started"

        match vm_status:
            case "timeout":
                status_icon = CROSS_SIGN_SYMBOL
                duration_str = f"{duration.seconds} seconds"
                status_str = "Timeout"

            case "already_started":
                status_icon = BLUE_CIRCLE_SYMBOL
                duration_str = f"Already running"
                status_str = "No action needed"

            case "dependency_failed":
                status_icon = FORBIDDEN_SIGN_SYMBOL
                duration_str = f"Dependency is not running"
                status_str = "Not started"

            case "disabled":
                status_icon = WARNING_SIGN_SYMBOL
                duration_str = f"Disabled in settings"
                status_str = "No action needed"

        msg = f"{DIGITS_SYMBOLS[self._status_count]} *{vm_type} {vm_id} ({vm_name})*:\n"
        msg += f"    - Start time: _{start_time.strftime('%H:%M:%S')}_\n"
        msg += f"    - Duration: _{duration_str}_\n"
        msg += f"    - Status: {status_icon} {status_str}\n\n"

        self._status_count += 1

        for message in self._message_notifier_map.keys():
            message.append(msg)

    def send(self):
        for message, notifier in self._message_notifier_map.items():
            LOGGER.debug(f"Send notification to {notifier}")
            notifier.send(message)

    def _create_notifier(self, notifier_config) -> Notifier:
        for key in notifier_config.keys():
            if key in notifier_types:
                LOGGER.debug(f"Creating '{key}' notifier.")
                return notifier_types[key](notifier_config[key])