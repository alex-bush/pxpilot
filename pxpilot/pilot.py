import warnings
from datetime import datetime

from pxpilot.config import ConfigManager
from pxpilot.config_validator import CONFIG_FILE
from pxpilot.logging_config import LOGGER
from pxpilot.notifications import NotificationManager
from pxpilot.notifications.notifier_types import NOTIFIER_TYPES
from pxpilot.pxtool import ProxmoxClient
from pxpilot.vm_management.executor import Executor
from pxpilot.vm_management.host_validator import HostValidator
from pxpilot.vm_management.vm_starter import VMStarter
from pxpilot.vm_status.executor import VmStatusChecker

warnings.filterwarnings("ignore")


def build_executor(app_config, notification_manager) -> Executor:
    px_client = ProxmoxClient(**app_config.proxmox_config.px_settings)

    starter = VMStarter(px_client, HostValidator())

    executor = Executor(px_client, app_config.proxmox_config.start_options, app_config.app_settings,
                        starter, notification_manager, False)

    return executor


def build_status_checker(app_config, notification_manager):
    px_client = ProxmoxClient(**app_config.proxmox_config.px_settings)

    status_checker = VmStatusChecker(px_client, notification_manager)

    return status_checker


def build_notification_manager(app_config) -> NotificationManager | None:
    if app_config.notification_settings is not None and len(app_config.notification_settings) > 0:
        return NotificationManager(app_config.notification_settings, NOTIFIER_TYPES)
    return None


def main(is_status_mode=False):
    app_config = ConfigManager().load(CONFIG_FILE)
    if app_config is not None:
        LOGGER.info("Config loaded.")

        notification_manager = build_notification_manager(app_config)

        if is_status_mode:
            status(app_config, notification_manager)
        else:
            execute(app_config, notification_manager)

        if notification_manager is not None:
            LOGGER.debug("Send notifications...")

            notification_manager.send()
    else:
        print("Config not loaded.")


def execute(app_config, notification_manager):
    try:
        executor = build_executor(app_config, notification_manager)
        executor.start()
    except Exception as ex:
        if notification_manager is not None:
            notification_manager.fatal(str(ex))
        LOGGER.error(ex)


def status(app_config, notification_manager: NotificationManager):
    try:
        st = build_status_checker(app_config, notification_manager)
        st.start()
    except Exception as ex:
        if notification_manager is not None:
            notification_manager.fatal(str(ex))
        LOGGER.error(ex)
