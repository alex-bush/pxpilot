# PX Pilot. Proxmox virtual machine launcher
**PXPilot**, an automation tool designed specifically for managing and orchestrating the startup of virtual machines in Proxmox environments. PXPilot streamlines complex startup sequences and ensures that dependencies between virtual machines are meticulously respected, addressing a gap in native Proxmox capabilities.

# Project Overview
PXPilot utilizes a configuration-driven approach to control the launch order and operational parameters of Proxmox virtual machines (VMs). This is especially useful in environments where the startup of certain VMs depends on the availability of others, such as ensuring a NAS storage server is running before initiating services that rely on it.

# Key Features
- Dependency Management: Ensures VMs start in the correct order based on predefined dependencies.
- Automated Notifications: Sends status summaries to Telegram, providing notifications about VM startup processes.
- Customizable Configuration: Users can easily define specific startup parameters and dependencies for each VM through a YAML configuration file.

# Installation

# Configuration
The configuration for this application is located in the `config.yaml` file, which is formatted in YAML. This file contains all necessary settings to connect to your Proxmox server and manage virtual machines (VMs). Before launching the application, please ensure that you have correctly configured access to your Proxmox environment and defined the list of VMs you intend to operate.

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
```yaml
settings:
  auto_shutdown: true  # Automatically shutdown the host where the pxpilot is located
  self_host:
    vm_id: 100
    node: "px-test"
    type: "lxc"  # Specify the type of VM (e.g., LXC, QEMU)
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
    node: "px-test"
    dependencies: []  # List VM IDs that must start before this VM
    startup_parameters:
      await_running: true  # Wait for VM to be fully up before proceeding
      startup_timeout: 60  # Timeout in seconds
    #dependencies: [] # Dependencies are optional
    healthcheck:
      target_url: "127.0.0.1"
      check_method: "ping"  # Use 'ping' or 'http' to check VM health
  - vm_id: 102
    node: "px-test"
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
    node: "px-test"
    type: "lxc"

notification_options:
  - telegram:
      token: 7022098123:BAH2pbAE5RueAGui43zO5wPjB5XJUWOxGsd
      chat_id: -4182361654

vms:
  - vm_id: 100
    node: px-test
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
    node: px-test
    dependencies:
      - 101  # required to be run before try to run this VM. 
```

</details>