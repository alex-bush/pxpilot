from .email import EmailNotifier
from .telegram import TelegramNotifier

# supported notifier, every new notifier should be added here
notifier_types = {
    'telegram': TelegramNotifier,
    'email': EmailNotifier,
}
