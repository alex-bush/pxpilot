import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Dict, Any

import sqlalchemy
from sqlalchemy.orm import sessionmaker, joinedload

from core.config import settings
from core.models import ProxmoxSettingsDbModel, VmStartupSettingsDbModel, NotifiersDbModel
from core.schemas.vms import VmStartupSettings
from pxpilot import pilot
from pxpilot.models.configuration.app_settings import AppSettings, ProxmoxSettings, CommonSettings
from pxpilot.models.configuration.vm_start_settings import VmStartOptions, HealthCheckOptions, HealthcheckType, \
    StartOptions

logger = logging.getLogger(__name__)


def pxpilot_worker():
    logger.debug('pxpilot worker has been starting')
    app_settings = get_settings()

    if app_settings is not None:
        logger.debug('app settings has been loaded. Starting pilot')
        pilot.start_from_settings(app_settings)


def run_pxpilot_worker() -> ThreadPoolExecutor:
    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(pxpilot_worker)

    return executor


def get_settings() -> Optional[AppSettings]:
    engine = sqlalchemy.create_engine(settings.db.connection_string)
    Session = sessionmaker(engine)

    px_settings = ProxmoxSettings()
    app_settings = CommonSettings()
    start_vms_settings: [VmStartupSettings()] = None
    notification_settings: Optional[Dict[str, Any]] = None

    with Session() as session:
        px_s = session.query(ProxmoxSettingsDbModel).first()
        if px_s is None:
            logger.info('Proxmox settings database does not exist')
            return

        px_settings.px_settings['host'] = px_s.hostname.replace("https://", "")
        px_settings.px_settings['token'] = px_s.token
        px_settings.px_settings['token_value'] = px_s.token_value
        px_settings.px_settings['verify_ssl'] = False  # px_s.extra_settings.

        vms = session.query(VmStartupSettingsDbModel) \
            .options(joinedload(VmStartupSettingsDbModel.healthcheck)) \
            .all()

        ntf = session.query(NotifiersDbModel).options(joinedload(NotifiersDbModel.options)).all()

    if vms is not None:
        start_vms_settings = convert_vms_to_vm_start_options(vms)
    else:
        logger.info('Startup settings are empty')

    if ntf is not None:
        notification_settings = convert_notification_settings(ntf)
    else:
        logger.info('Notification settings are empty')

    return AppSettings(app_settings=app_settings,
                       proxmox_settings=px_settings,
                       start_vms_settings=start_vms_settings,
                       notification_settings=notification_settings)


def convert_notification_settings(notifiers):
    notifiers_dict = {}

    for notifier in notifiers:
        notifier_settings = {}

        for option in notifier.options:
            if notifier.name == 'email':
                if option.name == 'smtp_server':
                    notifier_settings['smtp_server'] = option.value
                elif option.name == 'smtp_port':
                    notifier_settings['smtp_port'] = option.value
                elif option.name == 'smtp_user':
                    notifier_settings['smtp_user'] = option.value
                elif option.name == 'smtp_password':
                    notifier_settings['smtp_password'] = option.value
                elif option.name == 'from_email':
                    notifier_settings['from_email'] = option.value
                elif option.name == 'to_email':
                    notifier_settings['to_email'] = option.value

            elif notifier.name == 'telegram':
                if option.name == 'token':
                    notifier_settings['token'] = option.value
                elif option.name == 'chat_id':
                    notifier_settings['chat_id'] = option.value

        if notifier.enabled:
            notifiers_dict[notifier.name] = notifier_settings

    return notifiers_dict


def convert_vms_to_vm_start_options(vms) -> List[VmStartOptions]:
    vm_start_options_list = []
    for vm in vms:
        healthcheck_options = None
        if vm.healthcheck:
            first_healthcheck = vm.healthcheck[0] if vm.healthcheck else None
            if first_healthcheck:
                healthcheck_options = HealthCheckOptions(
                    target_url=first_healthcheck.target_url,
                    check_method=HealthcheckType(first_healthcheck.check_method)
                )

        start_options = StartOptions(
            enable_dependencies=vm.enable_dependencies,
            await_running=vm.wait_until_running,
            startup_timeout=vm.startup_timeout
        )

        vm_start_option = VmStartOptions(
            vm_id=vm.vm_id,
            enabled=vm.enabled,
            other={
                "name": vm.name,
                "description": vm.description,
                "node_name": vm.node_name,
            },
            startup_parameters=start_options,
            dependencies=[int(dep) for dep in (vm.dependencies or "").split(',') if dep],
            healthcheck=healthcheck_options
        )

        vm_start_options_list.append(vm_start_option)

    return vm_start_options_list
