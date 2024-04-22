import warnings

from pxvmflow.logging_config import LOGGER
from config import ConfigManager
from executor import Executor
from pxvmflow.host_validator import HostValidator
from pxvmflow.notifications import NotificationManager
from pxvmflow.pxtool import ProxmoxClient

warnings.filterwarnings("ignore")


def main():
    app_config = ConfigManager().load("config.yaml")
    if app_config is not None:
        LOGGER.info("Config loaded.")

        notification_manager = None
        if app_config.notification_options is not None and len(app_config.notification_options) > 0:
            notification_manager = NotificationManager(app_config.notification_options)

        px_client = ProxmoxClient(host=app_config.url, port=app_config.port, user=app_config.user,
                                  realm=app_config.realm, password=app_config.password, verify_ssl=app_config.verify_ssl)

        executor = Executor(px_client, app_config.start_options, HostValidator(), notification_manager)
        executor.start()

        if notification_manager is not None:
            LOGGER.debug("Notification Manager is non None. Try to send notifications")

            notification_manager.send()

    else:
        print("Config not loaded.")
