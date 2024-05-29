from pxpilot.notifications import NotificationManager
from pxpilot.pxtool import VMService


class VmStatusChecker:
    def __init__(self, vm_service: VMService, notification_manager: NotificationManager = None):
        self.vm_service = vm_service
        self.notification_manager = notification_manager

    def start(self):
        vms = self.vm_service.get_all_vms()
        for vm in vms:
            pass
