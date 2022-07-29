import asyncio
import datetime
import time

import mock
import pytest

from telegramfeed import entities
from telegramfeed.services.feeder_service import FeederService

TEST_FEED_URL = "https://blog.cleancoder.com/atom.xml"
TEST_FEED_LINK = "https://blog.cleancoder.com/foo/bar"


class TestFeederService:
    def setup(self):
        self.test_wait_time = 0.1

        self.mock_subscription_repo = mock.Mock()
        self.mock_chat_interface = mock.Mock()
        self.mock_feed_downloader_service = mock.Mock()

        self.feeder_service: FeederService = FeederService(
            self.mock_chat_interface,
            self.mock_subscription_repo,
            self.mock_feed_downloader_service,
            self.test_wait_time,
        )

    @pytest.mark.asyncio
    async def test_run_stop(self):
        self.mock_subscription_repo.fetch_all.return_value = []

        feeder_task = asyncio.Task(self.feeder_service.start())
        await asyncio.sleep(self.test_wait_time)
        self.feeder_service.stop()
        await feeder_task

    def test_process_feeds(self):
        self.mock_subscription_repo.fetch_all.return_value = [
            entities.Subscription(
                "123",
                TEST_FEED_URL,
                datetime.datetime.utcnow(),
            )
        ]

        self.mock_feed_downloader_service.download.return_value = {
            "entries": [
                {
                    "updated_parsed": time.gmtime(9999999999),
                    "link": TEST_FEED_LINK,
                },
            ]
        }

        self.feeder_service.process_feeds()

        self.mock_chat_interface.send_message.assert_called_with("123", TEST_FEED_LINK)

    def test_process_feeds_no_entries(self):
        self.mock_subscription_repo.fetch_all.return_value = [
            entities.Subscription(
                "123",
                TEST_FEED_URL,
                datetime.datetime.utcnow(),
            )
        ]

        self.mock_feed_downloader_service.download.return_value = {"entries": []}

        self.feeder_service.process_feeds()

    def test_chat_interface_send_message_error(self):
        self.mock_chat_interface.send_message.side_effect = Exception("Error")

        self.mock_subscription_repo.fetch_all.return_value = [
            entities.Subscription(
                "123",
                TEST_FEED_URL,
                datetime.datetime.utcnow(),
            )
        ]

        self.mock_feed_downloader_service.download.return_value = {
            "entries": [
                {
                    "updated_parsed": time.gmtime(9999999999),
                    "link": TEST_FEED_LINK,
                },
            ]
        }

        self.feeder_service.process_feeds()

    def test_process_feeds_no_entries_key(self):
        self.mock_subscription_repo.fetch_all.return_value = [
            entities.Subscription(
                "123",
                TEST_FEED_URL,
                datetime.datetime.utcnow(),
            )
        ]

        self.mock_feed_downloader_service.download.return_value = {}

        self.feeder_service.process_feeds()
