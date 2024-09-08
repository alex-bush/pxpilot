from core.models import NotifierSettingsDbModel, NotifiersDbModel
from core.schemas.notifications import Notifications, TelegramNotifier, EmailNotifier
from crud.notifications import get_notifiers, save_notifier
from services.base_service import BaseDbService


class NotificationService(BaseDbService):
    async def get_notificator(self) -> Notifications:
        notifiers = await get_notifiers(self._session)

        telegram_notifier = None
        email_notifier = None

        for notifier in notifiers:
            if notifier.name == 'telegram':
                options = {option.name: option.value for option in notifier.options}
                telegram_notifier = TelegramNotifier(
                    enabled=notifier.enabled,
                    chat_id=options.get('chat_id', ''),
                    token=options.get('token', '')
                )

            elif notifier.name == 'email':
                options = {option.name: option.value for option in notifier.options}
                email_notifier = EmailNotifier(
                    enabled=notifier.enabled,
                    smtp_server=options.get('smtp_server', ''),
                    smtp_port=int(options.get('smtp_port', 587)),
                    smtp_user=options.get('smtp_user', ''),
                    smtp_password=options.get('smtp_password', ''),
                    from_email=options.get('from_email', ''),
                    to_email=options.get('to_email', '')
                )

        return Notifications(
            telegram=telegram_notifier,
            email=email_notifier
        )

    async def save_notificator(self, notification: Notifications) -> None:
        notifiers = []

        if notification.telegram:
            telegram_options = [
                NotifierSettingsDbModel(name='chat_id', value=notification.telegram.chat_id),
                NotifierSettingsDbModel(name='token', value=notification.telegram.token)
            ]
            telegram_notifier = NotifiersDbModel(
                name='telegram',
                enabled=notification.telegram.enabled,
                options=telegram_options
            )
            notifiers.append(telegram_notifier)

        if notification.email:
            email_options = [
                NotifierSettingsDbModel(name='smtp_server', value=notification.email.smtp_server),
                NotifierSettingsDbModel(name='smtp_port', value=str(notification.email.smtp_port)),
                NotifierSettingsDbModel(name='smtp_user', value=notification.email.smtp_user),
                NotifierSettingsDbModel(name='smtp_password', value=notification.email.smtp_password),
                NotifierSettingsDbModel(name='from_email', value=notification.email.from_email),
                NotifierSettingsDbModel(name='to_email', value=notification.email.to_email)
            ]
            email_notifier = NotifiersDbModel(
                name='email',
                enabled=notification.email.enabled,
                options=email_options
            )
            notifiers.append(email_notifier)

        await save_notifier(notifiers, self._session)
