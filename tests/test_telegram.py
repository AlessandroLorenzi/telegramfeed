import os

import pytest
import requests_mock

from telegramfeed import services

from .fixtures.container import container


def test_send_message(container):
    telegram_service: services.TelegramService = container.telegram_service()
    user = os.getenv("TELEGRAM_USER")

    with requests_mock.Mocker() as mock:
        mock.post(
            f"https://api.telegram.org/bot{container.config.telegram_token()}/sendMessage",
            json={},
        )
        telegram_service.send_message(user, "Hello, world!")


def test_fetch_messages(container):
    telegram_service: services.TelegramService = container.telegram_service()

    with requests_mock.Mocker() as mock:
        mock.post(
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


def test_fetch_messages_empty(container):
    telegram_service: services.TelegramService = container.telegram_service()
    with requests_mock.Mocker() as mock:
        mock.post(
            f"https://api.telegram.org/bot{container.config.telegram_token()}/getUpdates",
            json={"result": []},
        )

        message = telegram_service.fetch_message(0)
    assert message is None


def test_fetch_messages_error(container):
    telegram_service: services.TelegramService = container.telegram_service()
    with requests_mock.Mocker() as mock:
        mock.post(
            f"https://api.telegram.org/bot{container.config.telegram_token()}/getUpdates",
            status_code=503,
            json={},
        )

        with pytest.raises(RuntimeError) as e:
            telegram_service.fetch_message(0)
        assert str(e.value) == "Telegram API call failed: {} - 503"
