from pxpilot.common import IConfig, ConfigProvider
from pxpilot.common.config_provider_v2 import ConfigProviderV2
from pxpilot.common.i_config import ConfigType


def get_config_provider(cfg_type: ConfigType, config_path) -> IConfig:
    if cfg_type is ConfigType.ruamel:
        return ConfigProviderV2.get_instance(config_path)
    return ConfigProvider(config_path)
