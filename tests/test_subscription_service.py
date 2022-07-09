import os

import pytest

from telegramfeed import entities, repositories
from telegramfeed.container import Container

from .fixtures.container import container


@pytest.mark.skip(reason="Before run: rm ./db.sqlite; alembic upgrade head")
def test_subscriptionmanager(container: Container):
    test_telegram_user = os.getenv("TELEGRAM_USER")
    subscription_repo = container.subscription_repo()
    telegram_service = container.telegram_service()
    subscription_service = container.subscription_service()

    telegram_service.send_message(test_telegram_user, "**We are starting a test**")

    subscription_service.process(generate_message("list"))
    subscription_service.process(
        generate_message("subscribe https://blog.cleancoder.com/atom.xml")
    )
    subscriptions_must_be_number(subscription_repo, 1)
    subscription_service.process(generate_message("list"))
    subscription_service.process(
        generate_message("subscribe https://www.reddit.com/r/python.rss")
    )
    subscription_service.process(
        generate_message("subscribe https://www.reddit.com/r/python.rss")
    )
    subscription_service.process(generate_message("list"))
    subscriptions_must_be_number(subscription_repo, 2)
    subscription_service.process(generate_message("help"))

    subscription_service.process(
        generate_message("unsubscribe https://www.reddit.com/r/python.rss")
    )
    subscription_service.process(generate_message("list"))
    subscriptions_must_be_number(subscription_repo, 1)
    subscription_service.process(
        generate_message("unsubscribe https://blog.cleancoder.com/atom.xml")
    )
    subscription_service.process(generate_message("list"))
    subscriptions_must_be_number(subscription_repo, 0)


def subscriptions_must_be_number(
    subscription_repo: repositories.SubscriptionRepo, number=0
):
    subscriptions = subscription_repo.fetch_all()
    assert number == len(subscriptions)


def generate_message(text: str) -> entities.UserMessage:
    test_telegram_user = os.getenv("TELEGRAM_USER")
    return entities.UserMessage(
        user_id=test_telegram_user,
        text=text,
        update_id=1,
    )
