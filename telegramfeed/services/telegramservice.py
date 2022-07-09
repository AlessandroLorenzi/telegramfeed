import json
import os
from typing import Optional

import requests

from telegramfeed import entities


class TelegramService:
    def __init__(self, token: Optional[str] = None):
        self.token = token

    def send_message(self, user: str, message: str):
        self.__post(
            "sendMessage", {"chat_id": user, "text": message, "parse_mode": "markdown"}
        )

    def fetch_message(self, offset: int = 0) -> Optional[entities.UserMessage]:
        response = self.__post("getUpdates", {"offset": offset})
        if len(response["result"]) == 0:
            return None
        return entities.UserMessage(
            user_id=response["result"][0]["message"]["from"]["id"],
            text=response["result"][0]["message"]["text"],
            update_id=response["result"][0]["update_id"],
        )

    def __post(self, method: str, body: dict) -> dict:
        url = f"https://api.telegram.org/bot{self.token}/{method}"
        headers = {"Content-Type": "application/json"}
        data = json.dumps(body)
        response = requests.post(url, headers=headers, data=data)
        if response.status_code != 200:
            raise RuntimeError(
                f"Telegram API call failed: {response.text} - {response.status_code}"
            )
        return response.json()
