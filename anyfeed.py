#!/usr/bin/env python3
import asyncio
import os
import sys

import feedparser
from sqlalchemy import create_engine

from telegramfeed import repositories, services

if __name__ == "__main__":
    cmd = sys.argv[1]

    # Inject Deps
    telegram_token = os.environ["TELEGRAM_TOKEN"]
    telegram_service = services.TelegramService(telegram_token)

    db_connection_string = os.environ["DB_CONNECTION_STRING"]
    engine = create_engine(db_connection_string)
    subscription_repo = repositories.SubscriptionRepo(engine)

    if cmd == "cron":
        feed_downloader_service = services.FeedDownloaderService(feedparser)
        feeder_service = services.FeederService(
            telegram_service, subscription_repo, feed_downloader_service
        )
        feeder_service.start()

    elif cmd == "chatbot":
        allowlist_users = os.environ["ALLOWLIST_USERS"].split(",")
        allowlist_service = services.AllowListService(allowlist_users)

        subscription_service = services.SubscriptionService(
            chat_interface=telegram_service,
            subscription_repo=subscription_repo,
            allowlist=allowlist_service,
        )
        asyncio.run(subscription_service.start())

    else:
        print("Invalid command")
