import inspect
from typing import List
from unittest.mock import patch, mock_open

import pytest
import yaml

from pxpilot.common.config_provider import IConfig
from pxpilot.common.config_provider_v2 import ConfigProviderV2
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


def get_full_method_path(cls, method_name):
    module_name = inspect.getmodule(cls).__name__
    return f"{module_name}.{cls.__name__}.{method_name}"


class TestConfigProviders:
    @pytest.mark.parametrize('target, patch_name', [
        (get_config_provider, 'yaml.safe_load'),
        (get_config_provider_ruamel, 'yaml.load')
    ])
    @patch(get_full_method_path(ConfigProviderV2, 'check_file_exists'), return_value=True)
    def test_load_proxmox_settings(self, mock_check_file_exists, target, patch_name):
        with patch("builtins.open", mock_open(read_data=VALID_CONFIG)):
            with patch(patch_name, return_value=yaml.safe_load(VALID_CONFIG)):
                with patch('copy.deepcopy', side_effect=lambda x: x):
                    cfg = target().load_px_settings()

                    self._assert_proxmox(cfg)

    @pytest.mark.parametrize('target, patch_name', [
        (get_config_provider, 'yaml.safe_load'),
        (get_config_provider_ruamel, 'yaml.load')
    ])
    @patch(get_full_method_path(ConfigProviderV2, 'check_file_exists'), return_value=True)
    def test_load_notification_options(self, mock_check_file_exists, target, patch_name):
        with patch("builtins.open", mock_open(read_data=VALID_CONFIG)):
            with patch(patch_name, return_value=yaml.safe_load(VALID_CONFIG)):
                with patch('copy.deepcopy', side_effect=lambda x: x):
                    cfg = target().load_notifications_settings()

                    self._assert_notifications(cfg)

    @pytest.mark.parametrize('target, patch_name', [
        (get_config_provider, 'yaml.safe_load'),
        (get_config_provider_ruamel, 'yaml.load')
    ])
    @patch(get_full_method_path(ConfigProviderV2, 'check_file_exists'), return_value=True)
    def test_load_vms_startups_options(self, mock_check_file_exists, target, patch_name):
        with patch("builtins.open", mock_open(read_data=VALID_CONFIG)):
            with patch(patch_name, return_value=yaml.safe_load(VALID_CONFIG)):
                with patch('copy.deepcopy', side_effect=lambda x: x):
                    cfg = target().load_start_vms_settings()

                    self._assert_vms(cfg)

    @pytest.mark.parametrize('target, patch_name', [
        (get_config_provider, 'yaml.safe_load'),
        (get_config_provider_ruamel, 'yaml.load')
    ])
    @patch(get_full_method_path(ConfigProviderV2, 'check_file_exists'), return_value=True)
    def test_load_app_config(self, mock_check_file_exists, target, patch_name):
        with patch("builtins.open", mock_open(read_data=VALID_CONFIG)):
            with patch(patch_name, return_value=yaml.safe_load(VALID_CONFIG)):
                with patch('copy.deepcopy', side_effect=lambda x: x):
                    cfg = target().get_app_config()

                    self._assert_proxmox(cfg.proxmox_settings)
                    self._assert_notifications(cfg.notification_settings)
                    self._assert_vms(cfg.start_vms_settings)

    @staticmethod
    def _assert_proxmox(cfg):
        assert isinstance(cfg, ProxmoxSettings)
        assert cfg.px_settings['host'] == HOST_VALUE
        assert cfg.px_settings['token'] == TOKEN_NAME_VALUE
        assert cfg.px_settings['token_value'] == TOKEN_VALUE

    @staticmethod
    def _assert_notifications(cfg):
        assert isinstance(cfg, dict)

        assert len(cfg) == 2

        assert isinstance(cfg, dict)
        assert isinstance(cfg['telegram'], dict)
        assert isinstance(cfg['email'], dict)

        assert cfg['telegram']['token'] == "7043"
        assert cfg['telegram']["chat_id"] == "14"

        assert cfg['email']['disabled'] is True
        assert cfg['email']['smtp_server'] == "mailjet.com"

    @staticmethod
    def _assert_vms(cfg: List[VmStartOptions]):
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
