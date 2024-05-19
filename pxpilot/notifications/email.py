import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .log import LOGGER
from .notifications import NotificationMessage, Notifier, ProxmoxMessage
from pxpilot.__about__ import __title__


class EmailMessage(ProxmoxMessage):
    def __init__(self):
        super().__init__()
        self.subject = f"{__title__} - "

    def add_header(self, start_time: datetime):
        self.subject += f"Proxmox VMs Startup Summary on {start_time.strftime('%d-%b-%Y')}"
        super().add_header(start_time)

    def fatal(self, error_message: str) -> None:
        self.subject = f"{__title__} - Proxmox VMs Startup Failed on {datetime.now().now().strftime('%d-%b-%Y')}"
        super().fatal(error_message)


class EmailNotifier(Notifier):
    def __init__(self, config):
        self._config = config

    def create_message(self) -> NotificationMessage:
        return EmailMessage()

    def send(self, message: NotificationMessage):
        msg = MIMEMultipart()
        msg["From"] = self._config["from_email"]
        msg["To"] = self._config["to_email"]
        msg["Subject"] = message.subject if isinstance(message, EmailMessage) else __title__

        msg.attach(MIMEText(message.message.replace('\n', '<br>'), 'html'))

        try:
            smtp = smtplib.SMTP(self._config["smtp_server"], self._config["smtp_port"])
            smtp.starttls()
            smtp.login(self._config["smtp_user"], self._config["smtp_password"])

            smtp.send_message(msg)

        except Exception as ex:
            LOGGER.error(f"{ex}")
        finally:
            smtp.quit()

        LOGGER.info("Email has been send successfully.")
