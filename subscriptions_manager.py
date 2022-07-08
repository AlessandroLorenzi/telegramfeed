#!/usr/bin/env python3
from telegramfeed import SubscriptionManager, Telegram, SubscriptionRepo
from sqlalchemy import create_engine
from time import sleep
import os

if __name__ == "__main__":
    telegram = Telegram()
    engine = create_engine(os.getenv("DB_CONNECTION_STRING"))
    subscription_repo = SubscriptionRepo(engine)
    subscriptionManager = SubscriptionManager(telegram, subscription_repo)

    message = {}
    offset = 0
    while True:
        message = telegram.fetch_message(offset)
        if message is None:
            sleep(1)
            continue
        offset = message.update_id + 1
        subscriptionManager.process(message)
