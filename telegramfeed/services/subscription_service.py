import asyncio
from time import sleep

from telegramfeed import entities, repositories, services

from .telegram_service import TelegramService

# TODO: extract command classes and inject them into the service

class SubscriptionService:
    def __init__(
        self,
        telegram: TelegramService,
        subscription_repo: repositories.SubscriptionRepo,
    ):
        self.telegram = telegram
        self.subscription_repo = subscription_repo

    async def start(self):
        print("SubscriptionService is listening for telegram messages...")
        self.request_to_stop = False
        offset = 0
        while not self.request_to_stop:
            message = self.telegram.fetch_message(offset)
            if message is None:
                await asyncio.sleep(1)
                continue
            offset = message.update_id + 1
            self.process(message)

    def stop(self):
        self.request_to_stop = True

    def subscribe(self, message: entities.UserMessage):
        feed_url = message.text.split(" ")[1]
        user_id = message.user_id

        subscription = entities.Subscription(user_id=user_id, feed_url=feed_url)

        try:
            self.subscription_repo.save(subscription)
        except Exception:
            self.telegram.send_message(
                user_id, f"You was alredy subscribed to {feed_url}!"
            )
            return
        self.telegram.send_message(user_id, f"You have been subscribed to {feed_url}!")

    def unsubscribe(self, message: entities.UserMessage):
        feed_url = message.text.split(" ")[1]
        user_id = message.user_id

        subscription = entities.Subscription(user_id=user_id, feed_url=feed_url)

        try:
            self.subscription_repo.delete(subscription)
        except Exception:
            self.telegram.send_message(user_id, f"You wasn't subscribed to {feed_url}!")
            return
        self.telegram.send_message(
            user_id, f"You have been unsubscribed from {feed_url}!"
        )

    def list(self, message: entities.UserMessage):

        user_id = message.user_id

        subs = self.subscription_repo.fetch_by_user_id(user_id)
        if len(subs) == 0:
            self.telegram.send_message(user_id, f"You have no subs!")
            return
        message = "Your subscriptions:\n"
        for sub in subs:
            message += f"- {sub.feed_url}\n"
        self.telegram.send_message(user_id, message)

    def send_helper(self, message: entities.UserMessage):
        helper = """Command available:
subscribe <feed>
list
"""
        self.telegram.send_message(message.user_id, helper)

    def process(self, message: entities.UserMessage):
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
