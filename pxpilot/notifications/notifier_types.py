from .telegram import TelegramNotifier

# supported notifier, every new notifier should be added here
notifier_types = {
    'telegram': TelegramNotifier,
}
