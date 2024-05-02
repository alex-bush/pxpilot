import warnings

from pxpilot.config import ConfigManager
from pxpilot.executor import Executor
from pxpilot.host_validator import HostValidator
from pxpilot.logging_config import LOGGER
from pxpilot.notifications import NotificationManager
from pxpilot.pxtool import ProxmoxClient
from pxpilot.pxtool.exceptions import ProxmoxConfigurationError, ProxmoxError
from pxpilot.vm_starter import VMStarter

warnings.filterwarnings("ignore")


def build_executor(app_config, notification_manager) -> Executor:
    px_client = ProxmoxClient(**app_config.proxmox_config.px_settings)

    starter = VMStarter(px_client, HostValidator())

    executor = Executor(px_client, app_config.proxmox_config.start_options, app_config.app_settings,
                        starter, notification_manager, False)

    return executor


def main():
    app_config = ConfigManager().load("config.yaml")
    if app_config is not None:
        LOGGER.info("Config loaded.")

        notification_manager = None
        if app_config.notification_settings is not None and len(app_config.notification_settings) > 0:
            notification_manager = NotificationManager(app_config.notification_settings)

        try:
            executor = build_executor(app_config, notification_manager)
            executor.start()
        except ProxmoxConfigurationError as ex:
            notification_manager.fatal(str(ex))
            LOGGER.error(ex)

        if notification_manager is not None:
            LOGGER.debug("Send notifications...")

            notification_manager.send()

    else:
        print("Config not loaded.")
