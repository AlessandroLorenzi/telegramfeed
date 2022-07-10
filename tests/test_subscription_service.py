import datetime
import os

import mock

from telegramfeed import entities, services
from telegramfeed.container import Container

from telegramfeed.container import Container
import asyncio
import pytest


class TestSubscriptionService:
    def setup(self):
        self.container = Container()
        self.container.config.db_connection_string.from_env("DB_CONNECTION_STRING")
        self.container.config.telegram_token.from_env("TELEGRAM_TOKEN")
        self.container.wire(modules=[__name__])

        self.mock_subscription_repo = mock.Mock()
        self.mock_telegram_service = mock.Mock()

        self.container.subscription_repo.override(self.mock_subscription_repo)
        self.container.telegram_service.override(self.mock_telegram_service)

        self.subscription_service: services.SubscriptionService = (
            self.container.subscription_service()
        )

    def test_subscribe(self):
        self.subscription_service.subscribe(
            self.generate_message("subscribe https://blog.cleancoder.com/atom.xml")
        )

        self.mock_subscription_repo.save.assert_called_once()
        self.mock_telegram_service.send_message.assert_called_once()

    def test_subscribe_exception(self):
        self.mock_subscription_repo.save.side_effect = Exception("Error")

        self.subscription_service.subscribe(
            self.generate_message("subscribe https://blog.cleancoder.com/atom.xml")
        )

        self.mock_subscription_repo.save.assert_called_once()
        self.mock_telegram_service.send_message.assert_called_once()

    def test_unsubscribe(self):
        self.subscription_service.unsubscribe(
            self.generate_message("unsubscribe https://blog.cleancoder.com/atom.xml")
        )

        self.mock_subscription_repo.delete.assert_called_once()
        self.mock_telegram_service.send_message.assert_called_once()

    def test_unsubscribe_exception(self):
        self.mock_subscription_repo.delete.side_effect = Exception("Error")

        self.subscription_service.unsubscribe(
            self.generate_message("unsubscribe https://blog.cleancoder.com/atom.xml")
        )

        self.mock_subscription_repo.delete.assert_called_once()
        self.mock_telegram_service.send_message.assert_called_once()

    def test_list_empty(self):

        self.mock_subscription_repo.fetch_by_user_id.return_value = []

        self.subscription_service.list(self.generate_message("list"))

        self.mock_subscription_repo.fetch_by_user_id.assert_called_once()
        self.mock_telegram_service.send_message.assert_called_once()

    def test_list_subs(self):
        self.mock_subscription_repo.fetch_by_user_id.return_value = [
            entities.Subscription(
                "123",
                "https://blog.cleancoder.com/atom.xml",
                datetime.datetime.utcnow(),
            ),
        ]

        self.subscription_service.list(self.generate_message("list"))

        self.mock_subscription_repo.fetch_by_user_id.assert_called_once()
        self.mock_telegram_service.send_message.assert_called_once()

    def test_send_helper(self):
        self.subscription_service.send_helper(self.generate_message("help"))

        self.mock_telegram_service.send_message.assert_called_once()

    def test_process_helper(self):
        self.subscription_service.process(self.generate_message("help"))

        self.mock_telegram_service.send_message.assert_called_once()

    def test_process_list(self):
        self.mock_subscription_repo.fetch_by_user_id.return_value = []

        self.subscription_service.process(self.generate_message("list"))

        self.mock_subscription_repo.fetch_by_user_id.assert_called_once()
        self.mock_telegram_service.send_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_stop(self):
        self.mock_telegram_service.fetch_message.side_effect = [
            self.generate_message("help"),
            None,
        ]

        task = asyncio.Task(self.subscription_service.start())
        await asyncio.sleep(1)

        self.subscription_service.stop()
        await task
        # await task
        self.mock_telegram_service.fetch_message.assert_has_calls([
            mock.call(0), # first contact with 0
            mock.call(2), # first message recived = 1, request from last message +1
        ])

    def generate_message(self, text: str) -> entities.UserMessage:
        test_telegram_user = os.getenv("TELEGRAM_USER")
        return entities.UserMessage(
            user_id=test_telegram_user,
            text=text,
            update_id=1,
        )
