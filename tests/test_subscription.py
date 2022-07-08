from telegramfeed import Subscription, SubscriptionRepo
from sqlalchemy import create_engine

import pytest
import os
import datetime


# TODO Mock engine!
@pytest.fixture
def engine():
    db_connection = os.getenv("DB_CONNECTION_STRING")
    engine = create_engine(db_connection)

    return engine


@pytest.fixture
def test_telegram_user():
    return os.getenv("TELEGRAM_USER")


@pytest.fixture
def reddit_sub(test_telegram_user):
    return Subscription(
        user_id=test_telegram_user, feed_url="https://www.reddit.com/r/python.rss"
    )


@pytest.fixture
def cleancoder_sub(test_telegram_user):
    return Subscription(
        user_id=test_telegram_user, feed_url="https://blog.cleancoder.com/atom.xml"
    )


class TestSubscription:
    # TODO one assert per test (after mock engine)
    @pytest.mark.skip(reason="Before run: rm ./db.sqlite; alembic upgrade head")
    def test_subscription(
        self,
        engine,
        reddit_sub: Subscription,
        cleancoder_sub: Subscription,
        test_telegram_user,
    ):
        subscription_repo = SubscriptionRepo(engine)

        subscription_repo.save(reddit_sub)
        self.subscriptions_must_be_number(subscription_repo, 1)

        subscription_repo.save(cleancoder_sub)
        self.subscriptions_must_be_number(subscription_repo, 2)

        subscription_repo.delete(cleancoder_sub)
        self.subscriptions_must_be_number(subscription_repo, 1)

        reddit_sub.last_check = datetime.datetime(2020, 1, 2, 10, 20, 30, 40)
        subscription_repo.update(reddit_sub)
        fetched_reddit_sub = subscription_repo.fetch_all()[0]

        assert fetched_reddit_sub.last_check == reddit_sub.last_check

        subscription_repo.save(cleancoder_sub)
        self.subscriptions_must_be_number(subscription_repo, 2)

        subs = subscription_repo.fetch_by_user_id(test_telegram_user)
        assert len(subs) == 2

    def subscriptions_must_be_number(
        self, subscription_repo: SubscriptionRepo, number=0
    ):
        subscriptions = subscription_repo.fetch_all()
        assert len(subscriptions) == number
