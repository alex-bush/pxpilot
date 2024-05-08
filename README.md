![project status](https://img.shields.io/badge/Project_status-In_development-green?logo=githubcopilot)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ghostkaa/pxpilot/main.yml?branch=main)

# PxPilot: Proxmox Virtual Machine Launcher
**PxPilot** is a tool designed to start Proxmox virtual machines (VMs) in a specified order according to a configuration file. The main features of PxPilot include checking dependencies before starting a virtual machine and sending notifications via email or Telegram about the results of the startup process.

**PxPilot** manages the startup of VMs so that they only boot up after the VMs on which they depend are already running. For example, if a VM requires Network Attached Storage (NAS) to store data, and the NAS is also a VM, we need to ensure the NAS is running before starting the VM.  
This project was created to address this challenge and, mainly, for educational purposes.

# Installation
For deployment, I chose to use either an LXC container on Proxmox or Docker. I decided against installing directly on the Proxmox host as I aim to keep the Proxmox instance clean and free of unnecessary installations. The main challenge is to detect the exact moment when Proxmox starts up; therefore, an LXC container with the auto-start option seemed like the perfect solution.  
Additionally, if there is a VM with Docker installed, which has no dependencies and needs to always be running, it is also a good candidate for hosting **PxPilot**.

Instructions coming soon...
# Configuration
The configuration for this application is located in the `config.yaml` file. This file contains all necessary settings to connect to your Proxmox server and manage virtual machines (VMs). Before launching the application, please ensure that you have correctly configured access to your Proxmox environment and defined the list of VMs you intend to operate.

Please follow the detailed sections below to configure your Proxmox access and VM management settings appropriately.

### Proxmox authentication settings
To interact with Proxmox services, ensure that the authentication credentials have the appropriate permissions. For detailed guidance on permissions, refer to the Proxmox documentation on (e.g. [PVE Permissions](https://pve.proxmox.com/wiki/User_Management#pveum_permission_management)).

#### Token Authentication
Use the following parameters to access Proxmox with a token:
```yaml
proxmox_config:
  host: "192.168.1.2:8006"  # proxmox host address with port
  token: "pxpilot@pve!pilot"  # token name in format username@pve|pam ! token name
  token_value: "c5f6f8e3-4627-4347-83a4-ee7cf6b4c0b5" # token secret
  verify_ssl: false
```
#### Username/Password Authentication
Alternatively, you can use username and password for authentication by specifying the following parameters:
```yaml
proxmox_config:
  host: "192.168.1.2:8006"  # Proxmox host address including port
  username: "user"
  realm: "pve"  # Authentication realm (e.g., 'pam', 'pve')
  password: "password"
  verify_ssl: true
```
In configurations where both token and username/password details are provided, the system will default to using the token for authentication.

## General Settings

General settings allow you to manage system behaviors such as automatic shutdowns and self-host settings.  
If PxPilot is deployed on a dedicated LXC container, there is no need to keep it running at all times. In this case, this option allows the container to be turned off after the application has finished running.
```yaml
settings:
  auto_shutdown: true  # Automatically shutdown the host where the pxpilot is located
  self_host:
    vm_id: 100
```
## Notification Settings

Configure notifications to be sent through different channels, enhancing monitoring and response capabilities.

Example configuration for Telegram notifications:

```yaml
notification_options:
  - telegram:
      token: "7022098123:BAH2pbAE5RueAGui43zO5wPjB5XJUWOxGsd"
      chat_id: "-4182361654"
```

## Virtual Machines (VMs) Configuration

Configure individual virtual machines with specific startup parameters, dependencies, and health checks to ensure operational reliability.
```yaml
vms:
  - vm_id: 100
    dependencies: []  # List VM IDs that must start before this VM
    startup_parameters:
      await_running: true  # Wait for VM to be fully up before proceeding
      startup_timeout: 60  # Timeout in seconds
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
    node: px-test
    startup_parameters:
      await_running: true
      startup_timeout: 60
    dependencies: []
    healthcheck:
      target_url: "http://127.0.0.1/"
      check_method: "http"

  - vm_id: 102
    dependencies:
      - 101  # required to be run before try to run this VM. 
```

</details>
