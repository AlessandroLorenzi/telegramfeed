#!/usr/bin/env python

import os

from sqlalchemy import create_engine, text

from telegramfeed import TelegramFeed
from telegramfeed.article import ArticleRepository
from telegramfeed.newsfeed import NewsFeed
from telegramfeed.telegram import TelegramService


def fetch_and_send(telegram_feed: TelegramFeed):
    telegram_feed.fetch_and_send()


if __name__ == "__main__":
    db_connection = os.environ.get("DB_CONNECTION_STRING")
    user = os.getenv("TELEGRAM_USER")

    engine = create_engine(db_connection)
    with engine.connect() as conn:
        conn.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS articles (
                url TEXT PRIMARY KEY,
                title TEXT,
                blog TEXT
            );
        """
            )
        )

    article_repository = ArticleRepository(engine)
    blogfeed = NewsFeed()
    telegram = TelegramService(user)

    telegram_feed = TelegramFeed(article_repository, blogfeed, telegram)
    telegram_feed.fetch_and_send()
