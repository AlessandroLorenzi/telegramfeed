import time

import mock
import pytest

from telegramfeed import services


class TestFeedDownloaderService:
    def setup(self):

        self.mock_feedparser = mock.Mock()
        self.feed_downloader_service = services.FeedDownloaderService(
            self.mock_feedparser
        )

    def test_download_feed(self):
        self.mock_feedparser.parse.return_value = {
            "feed": {
                "entries": [
                    {
                        "updated_parsed": time.gmtime(9999999999),
                        "link": "https://blog.cleancoder.com/foo/bar",
                    },
                ]
            }
        }

        feed_data = self.feed_downloader_service.download(
            "https://blog.cleancoder.com/atom.xml"
        )
        assert feed_data["feed"]["entries"] == [
            {
                "updated_parsed": time.gmtime(9999999999),
                "link": "https://blog.cleancoder.com/foo/bar",
            }
        ]

    def test_empty_feed(self):
        self.mock_feedparser.parse.return_value = {"feed": {}}

        with pytest.raises(RuntimeError):
            self.feed_downloader_service.download(
                "https://blog.cleancoder.com/atom.xml"
            )
