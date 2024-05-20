import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .log import LOGGER, get_metadata
from .notifications import NotificationMessage, Notifier, ProxmoxMessage


class EmailMessage(ProxmoxMessage):
    def __init__(self):
        super().__init__()

        self.title, self.version = get_metadata()
        self.subject = f"{self.title} - "

    def add_header(self, start_time: datetime):
        self.subject += f"Proxmox VMs Startup Summary on {start_time.strftime('%d-%b-%Y')}"
        super().add_header(start_time)

    def fatal(self, error_message: str) -> None:
        self.subject = f"{self.title} - Proxmox VMs Startup Failed on {datetime.now().now().strftime('%d-%b-%Y')}"
        super().fatal(error_message)

    def complete_message(self):
        self.message += f"<br><br><br>{self.title}_{self.version}"


class EmailNotifier(Notifier):
    def __init__(self, config):
        self._config = config
        self.title, self.version = get_metadata()

    def create_message(self) -> NotificationMessage:
        return EmailMessage()

    def send(self, message: NotificationMessage):
        if isinstance(message, EmailMessage):
            message.complete_message()

        msg = MIMEMultipart()
        msg["From"] = self._config["from_email"]
        msg["To"] = self._config["to_email"]
        msg["Subject"] = message.subject if isinstance(message, EmailMessage) else self.title

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
