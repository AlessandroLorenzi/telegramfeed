#!/usr/bin/env python3
import asyncio
import os
import signal
from typing import Any, List

import feedparser
from dependency_injector.wiring import Provide, inject
from sqlalchemy import create_engine

from telegramfeed import repositories, services
from telegramfeed.container import Container


class GracefulKiller:
    def __init__(self, tasks):
        self.tasks = tasks
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print("Ask to stop")
        for task in self.tasks:
            task.stop()


async def main(services: List[Any]):
    tasks = []
    for service in services:
        task = asyncio.Task(service.start())
        tasks.append(task)

    for task in tasks:
        await task

    print("Bye!")


if __name__ == "__main__":
    telegram_token = os.environ["TELEGRAM_TOKEN"]
    telegram_service = services.TelegramService(telegram_token)

    db_connection_string = os.environ["DB_CONNECTION_STRING"]
    engine = create_engine(db_connection_string)
    subscription_repo = repositories.SubscriptionRepo(engine)
    feed_downloader_service = services.FeedDownloaderService(feedparser)
    feeder_service = services.FeederService(
        telegram_service, subscription_repo, feed_downloader_service
    )

    subscription_service = services.SubscriptionService(
        chat_interface=telegram_service,
        subscription_repo=subscription_repo,
    )

    backgrownd_services: List[Any] = [feeder_service, subscription_service]

    GracefulKiller(backgrownd_services)

    # TODO: big catchall for all exceptions
    asyncio.run(main(backgrownd_services))
