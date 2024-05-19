![GitHub Actions Workflow Status](https://github.com/ghostkaa/pxpilot/actions/workflows/main.yml/badge.svg?branch=main)

# PxPilot: Proxmox Virtual Machine Launcher
[PxPilot](https://github.com/ghostkaa/pxpilot) is a tool designed to start [Proxmox](https://www.proxmox.com/en/proxmox-virtual-environment/overview) virtual machines (VMs) in a specified order according to a configuration file. 
It ensures VMs only boot up only if their dependencies are running, and sends notifications via email or Telegram about the startup process results.

# Features
- Dependency Management: Ensures VMs start in the correct order and start only if VMs on which they depend are already running.
- Notifications: Sends startup results via email or Telegram.

<details>
<summary>Overview</summary>

**PxPilot** manages the startup of VMs so that they only boot up after the VMs on which they depend are already running. For example, if a VM requires Network Attached Storage (NAS) to store data, and the NAS is also a VM, we need to ensure the NAS is running before starting the VM.  
This project was created to address this challenge and, mainly, for educational purposes.  
  
For deployment, I chose to use either an LXC container on Proxmox. I decided against installing directly on the Proxmox host as I aim to keep the Proxmox instance clean and free of unnecessary installations. The main challenge is to detect the exact moment when Proxmox starts up; therefore, an LXC container with the auto-start option seemed like the perfect solution.  

</details>

# Installation
### Create an LXC Container
- In Proxmox, create a new LXC container (Debian 12 recommended).
- Set the "Start at boot" option to "Yes".
- Ensure the LXC container has network access to the Proxmox API.
### Install PxPilot
Access your LXC container via SSH or the Proxmox console and run:
```
bash -c "$(wget -qLO - https://github.com/ghostkaa/pxpilot/raw/main/misc/install.sh)"
```
This command performs the following actions:
- Downloads the latest release of **PxPilot** in current folder.
- Install required packages: sudo(if not installed), python3.11-venv python3-pip
- Unpacks the files into a **pxpilot** folder.
- Sets up a Python virtual environment and installs dependencies.
- Configures **PxPilot** to start on container boot.

### Update PxPilot
To update PxPilot to latest version, run:
```
bash -c "$(wget -qLO - https://github.com/ghostkaa/pxpilot/raw/main/misc/update.sh)"
```
Previous version will be backed up into **pxpilot_backup** before updating.

# Configuration
Configure PxPilot in the config.yaml file. This file contains settings for connecting to your Proxmox server and managing VMs.

### Config validation
To check the configuration file, you can run PxPilot in validation mode:
```
python3 -m pxpilot [-v | --validate_config]
venv/bin/python3 -m pxpilot [-v | --validate_config]
```
In this mode, the configuration will be validated for the main parameters, and the connection to Proxmox will be checked.

### Proxmox authentication settings
To interact with Proxmox services, ensure that the authentication credentials have the appropriate permissions. For detailed guidance on permissions, refer to the Proxmox documentation on (e.g. [PVE Permissions](https://pve.proxmox.com/wiki/User_Management#pveum_permission_management)).

#### Token Authentication
```yaml
proxmox_config:
  host: "192.168.1.2:8006"  # proxmox host address with port
  token: "pxpilot@pve!pilot"  # token name in format username@pve|pam ! token name
  token_value: "c5f6f8e3-4627-4347-83a4-ee7cf6b4c0b5" # token secret
  verify_ssl: false
```
#### Username/Password Authentication
```yaml
proxmox_config:
  host: "192.168.1.2:8006"  # Proxmox host address including port
  username: "user"
  realm: "pve"  # Authentication realm (e.g., 'pam', 'pve')
  password: "password"
  verify_ssl: false
```
In configurations where both token and username/password details are provided, the system will default to using the token for authentication.
For more information about setting up the connection, please refer to the [Proxmoxer Documentation](https://proxmoxer.github.io/docs/latest/authentication/)

## General Settings

General settings allow you to manage system behaviors such as automatic shutdowns and self-host settings.  
It is possible to shutdown the pxpilot host(lxc) after start is completed. But be careful with this setting, it would be challenging to make some changes inside a container when this option is enabled 
```yaml
settings: #  optional
  auto_shutdown: true  # Automatically shutdown the host where the pxpilot is located
  self_host:
    vm_id: 100
```
## Notification Settings

Configure notifications to be sent through telegram or email.

Example configuration for Telegram and email notifications:

```yaml
notification_options:
  - telegram:
      token: "7022098123:BAH2pbAE5RueAGui43zO5wPjB5XJUWOxGsd" #  telegram bot token
      chat_id: "-4182361654" #  telegram chat id
  - email:
      smtp_server: "example.com"
      smtp_port: 587
      smtp_user: "user"
      smtp_password: "pwd"
      from_email: "pxpilot@example.com"
      to_email: "myemail@example.com"
```

## Virtual Machines (VMs) Configuration

Configure individual virtual machines with specific startup parameters, dependencies, and health checks.
```yaml
vms:
  - vm_id: 100
    dependencies: []  # List VM IDs that must start before this VM
    startup_parameters:
      await_running: true  # Wait for VM to be fully up before proceeding
      startup_timeout: 60  # Timeout in seconds. If the VM does not start within this time, the startup status will be set to 'failed'.
    #dependencies: [] # Dependencies are optional
    healthcheck:
      target_url: "127.0.0.1"
      check_method: "ping"  # Use 'ping' or 'http' to check VM health
  - vm_id: 102
    healthcheck:
      target_url: "http://127.0.0.1/"
      check_method: "http"
    dependencies:
      - 101  # VM 101 must be running before this VM can start
```

<details>
<summary>Config Example</summary>

```yaml
proxmox_config:
  host: "192.168.1.2:8006"
  token: "pxpilot@pve!pilot"
  token_value: "c5f6f8e9-4627-4345-83a4-ee7cf6b4c0b4"
  verify_ssl: false

settings:
  auto_shutdown: true  # shutdown the host where pxpilot is located
  self_host:
    vm_id: 100

notification_options:
  - telegram:
      token: 7022098123:BAH2pbAE5RueAGui43zO5wPjB5XJUWOxGsd
      chat_id: -4182361654

vms:
  - vm_id: 100
    dependencies: []
    startup_parameters:
      await_running: true  # false for start and go
      startup_timeout: 60
    healthcheck:  # healthcheck for validate that host is up and run
      target_url: "127.0.0.1"
      check_method: "ping"  # ping or http

  - vm_id: 101
    startup_parameters:
      await_running: true
      startup_timeout: 60
    dependencies: []
    healthcheck:
      target_url: "http://127.0.0.1/"
      check_method: "http"

  - vm_id: 102
    dependencies:
      - 101  # vm with id 101 is required to be run before run this VM 
```

</details>
