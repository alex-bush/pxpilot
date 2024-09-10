import logging
import warnings

from pxpilot.config.i_config import ConfigType
from pxpilot.models.configuration import config_builder
from pxpilot.notifications import NotificationManager
from pxpilot.notifications.notifier_types import NOTIFIER_TYPES
from pxpilot.pxtool import ProxmoxClient
from pxpilot.vm_management.executor import Executor
from pxpilot.vm_management.host_validator import HostValidator
from pxpilot.vm_management.vm_starter import VMStarter

warnings.filterwarnings("ignore")
logger = logging.getLogger(__name__)


def build_executor(app_config, notification_manager) -> Executor:
    px_client = ProxmoxClient(**app_config.proxmox_settings.px_settings)

    starter = VMStarter(px_client, HostValidator())

    executor = Executor(px_client, app_config.start_vms_settings, app_config.app_settings,
                        starter, notification_manager, False)

    return executor


def build_notification_manager(app_config) -> NotificationManager | None:
    if app_config.notification_settings is not None and len(app_config.notification_settings) > 0:
        return NotificationManager(app_config.notification_settings, NOTIFIER_TYPES)
    return None


def start(config_file):
    logger.info("pilot is starting...")

    config = config_builder.get_config_provider(ConfigType.ruamel, config_file)
    app_config = config.get_app_config()

    if app_config is not None:
        logger.info("Config loaded.")

        notification_manager = build_notification_manager(app_config)

        execute(app_config, notification_manager)

        if notification_manager is not None:
            logger.debug("Send notifications...")

            notification_manager.send()
    else:
        print("Config not loaded.")

    logger.info("pilot is completed. Exit.")


def execute(app_config, notification_manager):
    try:
        executor = build_executor(app_config, notification_manager)
        executor.start()
    except Exception as ex:
        if notification_manager is not None:
            notification_manager.fatal(str(ex))
        logger.error(ex)
