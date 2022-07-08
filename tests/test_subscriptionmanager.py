from telegramfeed import SubscriptionManager
import pytest
from telegramfeed import Telegram
from telegramfeed import Subscription, SubscriptionRepo
from telegramfeed import UserMessage

from sqlalchemy.sql.functions import now
from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Connectable
from sqlalchemy import create_engine
import os

# TODO Mock engine!
@pytest.fixture
def engine():
    db_connection = os.getenv("DB_CONNECTION_STRING")
    engine = create_engine(db_connection)

    return engine


@pytest.fixture
def test_telegram_user():
    return os.getenv("TELEGRAM_USER")


@pytest.mark.skip(reason="Before run: rm ./db.sqlite; alembic upgrade head")
def test_subscriptionmanager(engine, test_telegram_user):
    subscription_repo = SubscriptionRepo(engine)
    telegram = Telegram()

    subscription_manager = SubscriptionManager(telegram, subscription_repo)

    telegram.send_message(test_telegram_user, "**We are starting a test**")

    subscription_manager.process(generate_message("list"))
    subscription_manager.process(
        generate_message("subscribe https://blog.cleancoder.com/atom.xml")
    )
    subscriptions_must_be_number(subscription_repo, 1)
    subscription_manager.process(generate_message("list"))
    subscription_manager.process(
        generate_message("subscribe https://www.reddit.com/r/python.rss")
    )
    subscription_manager.process(
        generate_message("subscribe https://www.reddit.com/r/python.rss")
    )
    subscription_manager.process(generate_message("list"))
    subscriptions_must_be_number(subscription_repo, 2)
    subscription_manager.process(generate_message("help"))

    subscription_manager.process(
        generate_message("unsubscribe https://www.reddit.com/r/python.rss")
    )
    subscription_manager.process(generate_message("list"))
    subscriptions_must_be_number(subscription_repo, 1)
    subscription_manager.process(
        generate_message("unsubscribe https://blog.cleancoder.com/atom.xml")
    )
    subscription_manager.process(generate_message("list"))
    subscriptions_must_be_number(subscription_repo, 0)


def subscriptions_must_be_number(subscription_repo: SubscriptionRepo, number=0):
    subscriptions = subscription_repo.fetch_all()
    assert number == len(subscriptions)


def generate_message(text: str) -> UserMessage:
    test_telegram_user = os.getenv("TELEGRAM_USER")
    return UserMessage(
        user_id=test_telegram_user,
        text=text,
        update_id=1,
    )
