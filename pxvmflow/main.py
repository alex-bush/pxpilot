from config import VmFlowConfig
from executor import Executor

import warnings

from pxvmflow.logging_config import LOGGER
from pxvmflow.notifications import notifier_types, Notifier, TelegramMessage, NotificationManager
from pxvmflow.pxtool import ProxmoxClient

warnings.filterwarnings("ignore")


def create_notifier(notifier_config) -> Notifier:
    for key in notifier_config.keys():
        if key in notifier_types:
            return notifier_types[key](notifier_config[key])


def main():
    app_config = VmFlowConfig().load("config.yaml")
    if app_config is not None:
        LOGGER.info("Config loaded.")

        notification_manager = NotificationManager(app_config.notification_options)

        px_client = ProxmoxClient(host=app_config.url, port=app_config.port, user=app_config.user,
                                  realm=app_config.realm, password=app_config.password, verify_ssl=app_config.verify_ssl)
        executor = Executor(px_client, app_config.start_options, notification_manager)
        executor.start()

        if notification_manager is not None:
            LOGGER.debug("Notification Manager is non None. Try to send notifications")
            notification_manager.send()

        # message = TelegramMessage()
        # message.append("test message from pxvmflow")
        #
        # if message is not None:
        #     notifiers = [create_notifier(n) for n in app_config.notification_options]
        #
        #     for notifier in notifiers:
        #         notifier.send(message)


if __name__ == "__main__":
    main()
