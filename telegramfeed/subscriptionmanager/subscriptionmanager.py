from telegramfeed import Telegram
from telegramfeed import Subscription, SubscriptionRepo
from telegramfeed import UserMessage


class SubscriptionManager:
    def __init__(self, telegram: Telegram, subscription_repo: SubscriptionRepo):
        self.telegram = telegram
        self.subscription_repo = subscription_repo

    def subscribe(self, message: UserMessage):
        feed_url = message.text.split(" ")[1]
        user_id = message.user_id

        subscription = Subscription(user_id=user_id, feed_url=feed_url)

        try:
            self.subscription_repo.save(subscription)
        except Exception as e:
            self.telegram.send_message(
                user_id, f"You was alredy subscribed to {feed_url}!"
            )
            return
        self.telegram.send_message(user_id, f"You have been subscribed to {feed_url}!")

    def unsubscribe(self, message: UserMessage):
        feed_url = message.text.split(" ")[1]
        user_id = message.user_id

        subscription = Subscription(user_id=user_id, feed_url=feed_url)

        try:
            self.subscription_repo.delete(subscription)
        except Exception as e:
            self.telegram.send_message(user_id, f"You wasn't subscribed to {feed_url}!")
            return
        self.telegram.send_message(
            user_id, f"You have been unsubscribed from {feed_url}!"
        )

    def list(self, message: UserMessage):

        user_id = message.user_id

        subs = self.subscription_repo.fetch_by_user_id(user_id)
        if len(subs) == 0:
            self.telegram.send_message(user_id, f"You have no subs!")
            return
        message = "Your subscriptions:\n"
        for sub in subs:
            message += f"- {sub.feed_url}\n"
        self.telegram.send_message(user_id, message)

    def send_helper(self, message: UserMessage):
        helper = """Command available:
subscribe <feed>
list
"""
        self.telegram.send_message(message.user_id, helper)

    def process(self, message: UserMessage):
        functions = {
            "subscribe": self.subscribe,
            "list": self.list,
            "unsubscribe": self.unsubscribe,
        }

        command = message.text.split(" ")[0]
        if command not in functions:
            self.send_helper(message)
            return

        functions[command](message)
