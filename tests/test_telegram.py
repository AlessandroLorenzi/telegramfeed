import pytest
from telegramfeed.telegram import Telegram
import os


@pytest.fixture()
def telegram() -> Telegram:
    return Telegram()


@pytest.mark.skip(reason="Don't spam myself!")
class TestTelegram:
    def test_send_message(self, telegram: Telegram):
        user = os.getenv("TELEGRAM_USER")
        telegram.send_message(user, "Hello, world!")

    def test_fetch_messages(self, telegram: Telegram):
        message = {}
        offset = 0
        while message is not None:
            message = telegram.fetch_message(offset)
            if message is None:
                break
            assert message.user_id is not None
            assert message.text is not None
            assert message.update_id is not None
            offset = message.update_id + 1
