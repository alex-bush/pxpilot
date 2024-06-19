from typing import List
from unittest.mock import patch, mock_open

import pytest
import yaml
from ruamel.yaml import CommentedMap

from pxpilot.common.config_provider import IConfig
from pxpilot.common.i_config import ConfigType
from pxpilot.models.configuration import config_builder
from pxpilot.models.configuration.app_settings import ProxmoxSettings
from pxpilot.models.configuration.vm_start_settings import VmStartOptions, HealthcheckType

HOST_VALUE = "192.168.1.1:8006"
TOKEN_NAME_VALUE = "pxpilot@pve!pilot"
TOKEN_VALUE = "123"
VM_ID_1 = 100

VALID_CONFIG = f"""
proxmox_config:
  host: "{HOST_VALUE}"
  token: "{TOKEN_NAME_VALUE}"
  token_value: "{TOKEN_VALUE}"
  verify_ssl: false

settings:
  auto_start_dependency: false
  auto_shutdown: true
  self_host:
    vm_id: {VM_ID_1}
    node: "px-test"
    type: "lxc"

notification_options:
  telegram:
      token: "7043"
      chat_id: "14"
  email:
      disabled: True
      smtp_server: "mailjet.com"

vms:
  - vm_id: 100
    dependencies: []
    enabled: true
    startup_parameters:
      await_running: true
      startup_timeout: 60
    healthcheck:
      target_url: "192.168.1.2"
      check_method: "ping"

  - vm_id: 101
    startup_parameters:
      await_running: true
      startup_timeout: 10
    enabled: true
    dependencies: []
    healthcheck:
      target_url: "http://192.168.1.3/"
      check_method: "http"

  - vm_id: 102
    enabled: true
    dependencies:
      - 101
"""


def get_config_provider() -> IConfig:
    return config_builder.get_config_provider(ConfigType.yaml, "file_path")


def get_config_provider_ruamel() -> IConfig:
    return config_builder.get_config_provider(ConfigType.ruamel, "file_path")


@pytest.mark.parametrize('target, patch_name', [
    (get_config_provider, 'yaml.safe_load'),
    (get_config_provider_ruamel, 'yaml.load')
])
def test_load_proxmox_settings(target, patch_name):
    with patch("builtins.open", mock_open(read_data=VALID_CONFIG)):
        with patch(patch_name, return_value=yaml.safe_load(VALID_CONFIG)):
            cfg = target().load_px_settings()

            assert_proxmox(cfg)


@pytest.mark.parametrize('target, patch_name', [
    (get_config_provider, 'yaml.safe_load'),
    (get_config_provider_ruamel, 'yaml.load')
])
def test_load_notification_options(target, patch_name):
    with patch("builtins.open", mock_open(read_data=VALID_CONFIG)):
        with patch(patch_name, return_value=yaml.safe_load(VALID_CONFIG)):
            cfg = target().load_notifications_settings()

            assert_notifications(cfg)


@pytest.mark.parametrize('target, patch_name', [
    (get_config_provider, 'yaml.safe_load'),
    (get_config_provider_ruamel, 'yaml.load')
])
def test_load_vms_startups_options(target, patch_name):
    with patch("builtins.open", mock_open(read_data=VALID_CONFIG)):
        with patch(patch_name, return_value=yaml.safe_load(VALID_CONFIG)):
            cfg = target().load_start_vms_settings()

            assert_vms(cfg)


@pytest.mark.parametrize('target, patch_name', [
    (get_config_provider, 'yaml.safe_load'),
    (get_config_provider_ruamel, 'yaml.load')
])
def test_load_app_config(target, patch_name):
    with patch("builtins.open", mock_open(read_data=VALID_CONFIG)):
        with patch(patch_name, return_value=yaml.safe_load(VALID_CONFIG)):
            cfg = target().get_app_config()

            assert_proxmox(cfg.proxmox_settings)
            assert_notifications(cfg.notification_settings)
            assert_vms(cfg.start_vms_settings)


def assert_proxmox(cfg):
    assert isinstance(cfg, ProxmoxSettings)
    assert cfg.px_settings['host'] == HOST_VALUE
    assert cfg.px_settings['token'] == TOKEN_NAME_VALUE
    assert cfg.px_settings['token_value'] == TOKEN_VALUE


def assert_notifications(cfg):
    assert isinstance(cfg, dict)

    assert len(cfg) == 2

    assert isinstance(cfg, dict)
    assert isinstance(cfg['telegram'], dict)
    assert isinstance(cfg['email'], dict)

    assert cfg['telegram']['token'] == "7043"
    assert cfg['telegram']["chat_id"] == "14"

    assert cfg['email']['disabled'] is True
    assert cfg['email']['smtp_server'] == "mailjet.com"


def assert_vms(cfg: List[VmStartOptions]):
    assert len(cfg) == 3
    assert isinstance(cfg[0], VmStartOptions)

    assert cfg[0].vm_id == VM_ID_1
    assert cfg[0].enabled is True
    assert len(cfg[0].dependencies) == 0

    assert cfg[0].startup_parameters is not None
    assert cfg[0].startup_parameters.await_running is True

    assert cfg[0].healthcheck is not None
    assert isinstance(cfg[0].healthcheck.check_method, HealthcheckType)
    assert cfg[0].healthcheck.check_method.value == HealthcheckType.PING.value
    assert cfg[0].healthcheck.target_url == "192.168.1.2"
