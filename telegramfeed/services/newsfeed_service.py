import feedparser

from telegramfeed import Article


class NewsFeedService:
    def __init__(self, url) -> None:
        self.news_feed = feedparser.parse(url)
        self.title = self.news_feed.feed.title
        self.articles = []
        for entry in self.news_feed.entries:
            article = Article(entry.link, entry.title)
            self.articles.append(article)
