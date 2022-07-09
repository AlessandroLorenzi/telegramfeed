from datetime import datetime

from sqlalchemy import text

from telegramfeed import entities


class SubscriptionRepo:
    def __init__(self, engine) -> None:
        self.engine = engine

    def save(self, subscription: entities.Subscription) -> None:
        with self.engine.connect() as connection:
            connection.execute(
                text(
                    """
                INSERT INTO subscriptions (user_id, feed_url, last_check)
                VALUES (:user_id, :feed_url, :last_check)
            """
                ),
                {
                    "user_id": subscription.user_id,
                    "feed_url": subscription.feed_url,
                    "last_check": subscription.last_check,
                },
            )

    def fetch_all(self) -> list[entities.Subscription]:
        with self.engine.connect() as connection:
            result = connection.execute(
                text(
                    """
                SELECT * FROM subscriptions
            """
                )
            )

            return self.rows_to_subscriptions(result.fetchall())

    def fetch_by_user_id(self, user_id):
        with self.engine.connect() as connection:
            result = connection.execute(
                text(
                    """
                SELECT * FROM subscriptions
                WHERE user_id = :user_id
            """
                ),
                {"user_id": user_id},
            )
            return self.rows_to_subscriptions(result.fetchall())

    def rows_to_subscriptions(self, rows):
        return [
            entities.Subscription(
                user_id=row["user_id"],
                feed_url=row["feed_url"],
                last_check=datetime.strptime(row["last_check"], "%Y-%m-%d %H:%M:%S.%f"),
            )
            for row in rows
        ]

    def delete(self, subscription):
        with self.engine.connect() as connection:
            connection.execute(
                text(
                    """
                DELETE FROM subscriptions
                WHERE user_id = :user_id AND feed_url = :feed_url
            """
                ),
                {"user_id": subscription.user_id, "feed_url": subscription.feed_url},
            )

    def update(self, subscription):
        with self.engine.connect() as connection:
            connection.execute(
                text(
                    """
                UPDATE subscriptions
                SET last_check = :last_check
                WHERE user_id = :user_id AND feed_url = :feed_url
            """
                ),
                {
                    "user_id": subscription.user_id,
                    "feed_url": subscription.feed_url,
                    "last_check": subscription.last_check,
                },
            )
