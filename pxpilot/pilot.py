import warnings

from pxpilot.logging_config import LOGGER
from pxpilot.config import ConfigManager
from pxpilot.executor import Executor
from pxpilot.host_validator import HostValidator
from pxpilot.notifications import NotificationManager
from pxpilot.pxtool import ProxmoxClient

warnings.filterwarnings("ignore")


def main():
    app_config = ConfigManager().load("config.yaml")
    if app_config is not None:
        LOGGER.info("Config loaded.")

        notification_manager = None
        if app_config.notification_settings is not None and len(app_config.notification_settings) > 0:
            notification_manager = NotificationManager(app_config.notification_settings)

        px_client = ProxmoxClient(host=app_config.proxmox_config.url, port=app_config.proxmox_config.port,
                                  user=app_config.proxmox_config.user, realm=app_config.proxmox_config.realm,
                                  password=app_config.proxmox_config.password,
                                  verify_ssl=app_config.proxmox_config.verify_ssl)

        executor = Executor(px_client, app_config.proxmox_config.start_options, app_config.app_settings,
                            HostValidator(), notification_manager)
        executor.start()

        if notification_manager is not None:
            LOGGER.debug("Notification Manager is non None. Try to send notifications")

            notification_manager.send()

    else:
        print("Config not loaded.")
