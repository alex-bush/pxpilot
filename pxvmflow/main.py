from config import VmFlowConfig
from executor import Executor


def main():
    proxmox_config = VmFlowConfig().load("config.yaml")
    if proxmox_config is not None:
        print("Config loaded. Proceed to execution")
        executor = Executor(proxmox_config)
        #executor.start()


if __name__ == "__main__":
    main()
