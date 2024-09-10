from .email import EmailNotifier
from .telegram import TelegramNotifier

# supported notifier, every new notifier should be added here
NOTIFIER_TYPES = {
    'telegram': TelegramNotifier,
    'email': EmailNotifier,
}
