from config import VmFlowConfig
from executor import Executor

import warnings

from pxvmflow.logging_config import LOGGER

warnings.filterwarnings("ignore")


def main():
    proxmox_config = VmFlowConfig().load("config.yaml")
    if proxmox_config is not None:
        LOGGER.info("Config loaded.")

        executor = Executor(proxmox_config)
        executor.start()


if __name__ == "__main__":
    main()
