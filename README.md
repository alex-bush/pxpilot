# PX Pilot. Proxmox virtual machine launcher
**PXPilot**, an automation tool designed specifically for managing and orchestrating the startup of virtual machines in Proxmox environments. PXPilot streamlines complex startup sequences and ensures that dependencies between virtual machines are meticulously respected, addressing a gap in native Proxmox capabilities.

# Project Overview
PXPilot utilizes a configuration-driven approach to control the launch order and operational parameters of Proxmox virtual machines (VMs). This is especially useful in environments where the startup of certain VMs depends on the availability of others, such as ensuring a NAS storage server is running before initiating services that rely on it.

# Key Features
- Dependency Management: Ensures VMs start in the correct order based on predefined dependencies.
- Automated Notifications: Sends status summaries to Telegram, providing notifications about VM startup processes.
- Customizable Configuration: Users can easily define specific startup parameters and dependencies for each VM through a YAML configuration file.
