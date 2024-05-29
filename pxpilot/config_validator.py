from typing import List

from pxpilot.config import ConfigManager, CONFIG_FILE
from pxpilot.pxtool import ProxmoxClient
from pxpilot.vm_management.models import VMLaunchSettings


def validate_config():
    print(f"Start validating '{CONFIG_FILE}'...")
    valid = True
    try:
        app_config = ConfigManager().load(CONFIG_FILE)
        print("Config loaded.")

        if app_config.proxmox_config is None or app_config.proxmox_config.px_settings is None:
            valid = False
            print("(!) Proxmox access config is missing.")

        if app_config.app_settings is None:
            print("(!) Optional App setting section is missing")

        if app_config.proxmox_config is not None:
            if app_config.proxmox_config.start_options is None or len(app_config.proxmox_config.start_options) == 0:
                print("(!) There is no VM's to start in config")

        if app_config.notification_settings is None or len(app_config.notification_settings) == 0:
            print("(!) Notification settings are missed")

        valid = validate_proxmox_config(app_config.proxmox_config.px_settings)

        validate_vms(app_config.proxmox_config.start_options)

        if valid:
            print("Config validated successfully.")
        else:
            print("Config validated with errors.")
    except Exception as ex:
        print(f"(!) Error occurred during reading config: {ex}")


def validate_connection(px_settings) -> bool:
    print("  Try to connect to Proxmox...")
    px_client = ProxmoxClient(**px_settings)
    try:
        px_client.get_all_vms()
        print("    Successfully connected.")
    except Exception as ex:
        print(f"    (!) Unable to connect to Proxmox: {ex}")
        return False
    return True


def validate_proxmox_config(px_settings) -> bool:
    print("⌜ Proxmox settings validation: starting...")
    host_status: str
    valid = False
    host = px_settings.get("host", None)
    if host is not None:
        if len(host) > 0:
            valid = True
            host_status = "Ok"
        else:
            host_status = "Empty"
    else:
        host_status = "Missing"

    print(f"  Proxmox host: {host_status}")

    token = px_settings.get("token", None)
    token_value = px_settings.get("token_value", None)
    user = px_settings.get("user", None)
    password = px_settings.get("password", None)
    realm = px_settings.get("realm", None)

    auth_valid = False

    if token and token_value:
        if len(token) > 0 and len(token_value) > 0:
            auth_valid = True
            auth_status = "Ok (Token-based)"
        else:
            auth_status = "Invalid Token or Token Value"
    elif user and password and realm:
        if len(user) > 0 and len(password) > 0 and len(realm) > 0:
            auth_valid = True
            auth_status = "Ok (User-password-based)"
        else:
            auth_status = "Invalid User, Password, or Realm"
    else:
        auth_status = "Missing Authentication Information"

    print(f"  Proxmox authentication: {auth_status}")

    valid = valid and auth_valid

    if valid:
        valid = valid and validate_connection(px_settings)

    print("∟ Proxmox settings validation: completed.")
    return valid


def validate_vms(starts: List[VMLaunchSettings]):
    print("⌜ Start settings validation: starting...")
    valid = False

    print(f"  Found {len(starts)} vm start settings.")

    for vm in starts:
        if vm.vm_id is None or vm.vm_id == 0 or not isinstance(vm.vm_id, int):
            print(f"  (!) Wrong VM id: {vm.vm_id}")

    print("∟ Start settings validation: completed.")
    return valid
