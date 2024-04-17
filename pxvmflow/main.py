from config import VmFlowConfig
from executor import Executor
from consts import LOGGER

import warnings
warnings.filterwarnings("ignore")


def main():
    proxmox_config = VmFlowConfig().load("config.yaml")
    if proxmox_config is not None:
        LOGGER.info("Config loaded.")

        executor = Executor(proxmox_config)
        executor.start()


if __name__ == "__main__":
    main()
