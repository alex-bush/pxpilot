# import re
# from datetime import datetime, timedelta
#
# import requests
# from typing import Protocol
#
# __all__ = ["NotificationMessage", "Notifier", "TelegramNotifier", "notifier_types", "NotificationManager"]
#
# from pxvmflow.logging_config import LOGGER
#
#
# class NotificationMessage(Protocol):
#     def get(self) -> str:
#         pass
#
#     def append(self, string: str):
#         pass
#
#
# class TelegramMessage(NotificationMessage):
#     def __init__(self):
#         self._message = str()
#
#     def get(self) -> str:
#         return self._message
#
#     def append(self, string: str):
#         self._message += string
#
#
# class Notifier(Protocol):
#     def get_message(self) -> NotificationMessage:
#         pass
#
#     def send(self, message: NotificationMessage):
#         pass
#
#
# class TelegramNotifier(Notifier):
#     def __init__(self, config):
#         self._config = config
#
#     def get_message(self) -> NotificationMessage:
#         return TelegramMessage()
#
#     def escape(self, text):
#         special_chars = "[]()~`>#+-=|{}.!"
#         pattern = re.compile(r'([' + re.escape(special_chars) + '])')
#         return pattern.sub(r'\\\1', text)
#
#     def send(self, message: NotificationMessage):
#         url = f'https://api.telegram.org/bot{self._config['token']}/sendMessage?chat_id={self._config['chat_id']}&parse_mode=MarkdownV2'
#
#         msg = self.escape(message.get())
#
#         response = requests.post(url, json={'text': msg}, timeout=10)
#
#         match response.status_code:
#             case 200:
#                 LOGGER.info("Notification has been send successfully.")
#             case 400:
#                 LOGGER.warn("Bad request. " + response.text)
#             case 401:
#                 LOGGER.warn("Cannot access to noti")
#
#
# notifier_types = {
#     'telegram': TelegramNotifier,
# }
#
#
# class NotificationManager:
#     def __init__(self, config):
#         self._status_count = 0
#         self._rocket = "\U0001F680"
#         self._check_mark = "\U00002705"
#         self._blue_circle = "\U0001F535"
#         self._digits = ["\U00000031\U0000FE0F\U000020E3", "\U00000032\U0000FE0F\U000020E3", "\U00000033\U0000FE0F\U000020E3",
#                   "\U00000034\U0000FE0F\U000020E3", "\U00000035\U0000FE0F\U000020E3", "\U00000036\U0000FE0F\U000020E3",
#                   "\U00000037\U0000FE0F\U000020E3", "\U00000038\U0000FE0F\U000020E3", "\U00000039\U0000FE0F\U000020E3"]
#
#         self._notifiers = [self._create_notifier(n) for n in config]
#         self._message_notifier_map = {n.get_message(): n for n in self._notifiers}
#
#     def start(self, start_time: datetime):
#         """
#
#         :param start_time:
#         """
#         for message in self._message_notifier_map.keys():
#             msg = f"{self._rocket} *Proxmox VMs Startup Summary* - Start Time: _{start_time.strftime("%d-%b-%Y %H:%M:%S")}_\n\n"
#             message.append(msg)
#
#     def append_status(self, vm_type, vm_id, vm_name, vm_status, start_time, duration: timedelta):
#         """
#
#         :param vm_type:
#         :param vm_id:
#         :param name:
#         :param status:
#         :param start_time:
#         :param duration:
#         """
#         if vm_status == "started":
#             status_icon = self._check_mark
#             duration_str = f"{duration.seconds} seconds"
#             status_str = "Successfully started"
#         else:
#             status_icon = self._blue_circle
#             duration_str = f"Already running"
#             status_str = "No action needed"
#
#         msg = f"{self._digits[self._status_count]} *{vm_type} {vm_id} ({vm_name})*:\n"
#         msg += f"    - Start time: _{start_time.strftime("%H:%M:%S")}_\n"
#         msg += f"    - Duration: _{duration_str}_\n"
#         msg += f"    - Status: {status_icon} {status_str}\n\n"
#
#         self._status_count += 1
#
#         for message in self._message_notifier_map.keys():
#             message.append(msg)
#
#     def send(self):
#         for message, notifier in self._message_notifier_map.items():
#             LOGGER.debug(f"Send notification to {notifier}")
#             notifier.send(message)
#
#     def _create_notifier(self, notifier_config) -> Notifier:
#         for key in notifier_config.keys():
#             if key in notifier_types:
#                 LOGGER.debug(f"Creating '{key}' notifier.")
#                 return notifier_types[key](notifier_config[key])
