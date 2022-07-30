import os

import pytest
import requests_mock

from telegramfeed import services


class TestTelegramService:
    def setup(self):
        self.test_token = "123"
        self.telegram_service = services.TelegramService(
            self.test_token,
        )

    def test_send_message(self):
        user = os.getenv("TELEGRAM_USER")

        with requests_mock.Mocker() as mock:
            mock.post(
                f"https://api.telegram.org/bot{self.test_token}/sendMessage",
                json={},
            )
            self.telegram_service.send_message(user, "Hello, world!")

    def test_fetch_messages(self):

        with requests_mock.Mocker() as mock:
            mock.post(
                f"https://api.telegram.org/bot{self.test_token}/getUpdates",
                json={
                    "result": [
                        {
                            "update_id": 1111,
                            "message": {"text": "hello", "from": {"id": "123"}},
                        }
                    ]
                },
            )
            message = self.telegram_service.fetch_message(0)

        assert message.user_id is not None
        assert message.text is not None
        assert message.update_id is not None

    def test_fetch_messages_empty(self):
        with requests_mock.Mocker() as mock:
            mock.post(
                f"https://api.telegram.org/bot{self.test_token}/getUpdates",
                json={"result": []},
            )

            message = self.telegram_service.fetch_message(0)
        assert message is None

    def test_fetch_messages_error(self):
        with requests_mock.Mocker() as mock:
            mock.post(
                f"https://api.telegram.org/bot{self.test_token}/getUpdates",
                status_code=503,
                json={},
            )

            with pytest.raises(RuntimeError) as e:
                self.telegram_service.fetch_message(0)
            assert str(e.value) == "Telegram API call failed: {} - 503"
