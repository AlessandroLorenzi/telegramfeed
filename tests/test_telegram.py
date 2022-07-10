import os

import pytest

from telegramfeed import services

from .fixtures.container import container


def test_send_message(container, requests_mock):
    telegram_service: services.TelegramService = container.telegram_service()
    user = os.getenv("TELEGRAM_USER")
    requests_mock.post(
        f"https://api.telegram.org/bot{container.config.telegram_token()}/sendMessage",
        json={},
    )

    telegram_service.send_message(user, "Hello, world!")


def test_fetch_messages(container, requests_mock):
    telegram_service = container.telegram_service()

    requests_mock.post(
        f"https://api.telegram.org/bot{container.config.telegram_token()}/getUpdates",
        json={
            "result": [
                {
                    "update_id": 1111,
                    "message": {"text": "hello", "from": {"id": "123"}},
                }
            ]
        },
    )

    message = telegram_service.fetch_message(0)
    assert message.user_id is not None
    assert message.text is not None
    assert message.update_id is not None
