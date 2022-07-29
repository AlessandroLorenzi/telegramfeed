from typing import Any


class FeedDownloaderService:
    def __init__(self, feedparser: Any):
        self.feedparser = feedparser

    def download(self, feed_url: str) -> object:
        feed_data = self.feedparser.parse(feed_url)
        if feed_data["feed"] == {}:
            raise RuntimeError("Feed not valid")
        return feed_data
