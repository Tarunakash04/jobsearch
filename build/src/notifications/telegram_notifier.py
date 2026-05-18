import os
import requests

from dotenv import load_dotenv

load_dotenv()


class TelegramNotifier:

    def __init__(self):

        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not self.bot_token:
            raise Exception("Missing TELEGRAM_BOT_TOKEN")

        if not self.chat_id:
            raise Exception("Missing TELEGRAM_CHAT_ID")

        self.base_url = (
            f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        )

    def send_message(self, message: str):

        payload = {
            "chat_id": self.chat_id,
            "text": message,
        }

        response = requests.post(
            self.base_url,
            json=payload,
            timeout=10
        )

        if response.status_code != 200:
            raise Exception(
                f"Telegram API failed: {response.text}"
            )

        return response.json()