import datetime
import os

import pytest
from sqlalchemy import create_engine

from telegramfeed import entities, repositories
from telegramfeed.container import Container

from .fixtures.container import container


@pytest.fixture
def test_telegram_user():
    return os.getenv("TELEGRAM_USER")


@pytest.fixture
def reddit_sub(test_telegram_user):
    return entities.Subscription(
        user_id=test_telegram_user, feed_url="https://www.reddit.com/r/python.rss"
    )


@pytest.fixture
def cleancoder_sub(test_telegram_user):
    return entities.Subscription(
        user_id=test_telegram_user, feed_url="https://blog.cleancoder.com/atom.xml"
    )


# TODO one assert per test (after mock engine)
@pytest.mark.skip(reason="Before run: rm ./db.sqlite; alembic upgrade head")
def test_subscription(
    reddit_sub: entities.Subscription,
    cleancoder_sub: entities.Subscription,
    container: Container,
    test_telegram_user,
):
    subscription_repo = container.subscription_repo()

    subscription_repo.save(reddit_sub)
    subscriptions_must_be_number(subscription_repo, 1)

    subscription_repo.save(cleancoder_sub)
    subscriptions_must_be_number(subscription_repo, 2)

    subscription_repo.delete(cleancoder_sub)
    subscriptions_must_be_number(subscription_repo, 1)

    reddit_sub.last_check = datetime.datetime(2020, 1, 2, 10, 20, 30, 40)
    subscription_repo.update(reddit_sub)
    fetched_reddit_sub = subscription_repo.fetch_all()[0]

    assert fetched_reddit_sub.last_check == reddit_sub.last_check

    subscription_repo.save(cleancoder_sub)
    subscriptions_must_be_number(subscription_repo, 2)

    subs = subscription_repo.fetch_by_user_id(test_telegram_user)
    assert len(subs) == 2


def subscriptions_must_be_number(
    subscription_repo: repositories.SubscriptionRepo, number=0
):
    subscriptions = subscription_repo.fetch_all()
    assert len(subscriptions) == number
