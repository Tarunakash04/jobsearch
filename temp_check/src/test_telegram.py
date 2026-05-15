from src.notifications.telegram_notifier import TelegramNotifier


def main():

    notifier = TelegramNotifier()

    notifier.send_message(
        "🚀 ApplySei test alert successful"
    )

    print("Telegram test message sent")


if __name__ == "__main__":
    main()