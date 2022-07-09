import os

import pytest

from .fixtures.container import container


@pytest.mark.skip(reason="Don't spam myself!")
def test_send_message(container):
    telegram_service = container.telegram_service()
    user = os.getenv("TELEGRAM_USER")
    telegram_service.send_message(user, "Hello, world!")


@pytest.mark.skip(reason="Don't spam myself!")
def test_fetch_messages(container):
    telegram_service = container.telegram_service()
    message = {}
    offset = 0
    while message is not None:
        message = telegram_service.fetch_message(offset)
        if message is None:
            break
        assert message.user_id is not None
        assert message.text is not None
        assert message.update_id is not None
        offset = message.update_id + 1
