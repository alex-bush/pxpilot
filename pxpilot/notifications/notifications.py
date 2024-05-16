from datetime import datetime, timedelta
from typing import Protocol

from pxpilot.notifications.consts import ROCKET_SYMBOL, HOURGLASS_NOT_DONE_SYMBOL, CHECK_MARK_SYMBOL, \
    CROSS_SIGN_SYMBOL, BLUE_CIRCLE_SYMBOL, FORBIDDEN_SIGN_SYMBOL, WARNING_SIGN_SYMBOL, DIGITS_SYMBOLS, STOP_SIGN_SYMBOL


class NotificationMessage:
    """ Container for building notification messages incrementally. """

    def __init__(self):
        self._notification_message = str()

    @property
    def mode(self):
        return "HTML"

    @property
    def message(self):
        return self._notification_message

    @message.setter
    def message(self, value):
        self._notification_message = value

    def add_header(self, start_time: datetime):
        pass

    def append_vm_status(self, vm_type, vm_id, vm_name, vm_status, start_time, duration: timedelta):
        pass

    def append_error(self, error_message: str) -> None:
        pass

    def fatal(self, error_message: str) -> None:
        pass


class ProxmoxMessage(NotificationMessage):
    def __init__(self):
        super().__init__()
        self._status_count = 0

    def add_header(self, start_time: datetime):
        self.message += f"{ROCKET_SYMBOL} <b>Proxmox VMs Startup Summary</b>\n"
        self.message += f"Date: <i>{start_time.strftime('%d-%b-%Y')}</i>\n"
        self.message += f"Time: <i>{start_time.strftime('%H:%M:%S')}</i>\n\n"

    def append_vm_status(self, vm_type, vm_id, vm_name, vm_status, start_time, duration: timedelta):
        status_icon = HOURGLASS_NOT_DONE_SYMBOL
        duration_str = status_str = "unknown"

        match vm_status:
            case "started":
                status_icon = CHECK_MARK_SYMBOL
                duration_str = f"{duration.seconds} seconds"
                status_str = "Successfully started"
            case "timeout":
                status_icon = CROSS_SIGN_SYMBOL
                duration_str = f"{duration.seconds} seconds"
                status_str = "Timeout"
            case "already_started":
                status_icon = BLUE_CIRCLE_SYMBOL
                duration_str = "Already running"
                status_str = "No action needed"
            case "dependency_failed":
                status_icon = FORBIDDEN_SIGN_SYMBOL
                duration_str = "Dependency is not running"
                status_str = "Not started"
            case "disabled":
                status_icon = WARNING_SIGN_SYMBOL
                duration_str = "Disabled in settings"
                status_str = "No action needed"

        msg = f"{DIGITS_SYMBOLS[self._status_count]} <b>{vm_name}</b>:\n"
        msg += f"    - ID: {vm_id} ({vm_type})\n"
        msg += f"    - Start time: <i>{start_time.strftime('%H:%M:%S')}</i>\n"
        msg += f"    - Duration: <i>{duration_str}</i>\n"
        msg += f"    - Status: {status_icon} {status_str}\n\n"

        self._status_count += 1

        self.message += msg

    def append_error(self, error_message: str) -> None:
        msg = f"{STOP_SIGN_SYMBOL} <b>Failed</b>: {error_message}"
        self.message += msg

    def fatal(self, error_message: str) -> None:
        self.message = ""

        self.message += f"{STOP_SIGN_SYMBOL} <b>Proxmox VMs Startup Failed</b>\n"
        self.message += f"Date: <i>{datetime.now().strftime('%d-%b-%Y')}</i>\n"
        self.message += f"Time: <i>{datetime.now().strftime('%H:%M:%S')}</i>\n\n"
        self.message += error_message


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
