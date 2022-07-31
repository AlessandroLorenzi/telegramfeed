import asyncio

from telegramfeed import entities, interfaces, repositories

from .allowlist_service import AllowListService

# TODO: extract command classes and inject them into the service


class SubscriptionService:
    def __init__(
        self,
        chat_interface: interfaces.ChatInterface,
        subscription_repo: repositories.SubscriptionRepo,
        allowlist: AllowListService,
    ):
        self.chat_interface = chat_interface
        self.subscription_repo = subscription_repo
        self.allowlist = allowlist

    async def start(self):
        print("SubscriptionService is listening for messages...")
        self.request_to_stop = False
        offset = 0
        while not self.request_to_stop:
            message = self.chat_interface.fetch_message(offset)
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
            self.chat_interface.send_message(
                user_id, f"You was alredy subscribed to {feed_url}!"
            )
            return
        self.chat_interface.send_message(
            user_id, f"You have been subscribed to {feed_url}!"
        )

    def unsubscribe(self, message: entities.UserMessage):
        feed_url = message.text.split(" ")[1]
        user_id = message.user_id

        subscription = entities.Subscription(user_id=user_id, feed_url=feed_url)

        try:
            self.subscription_repo.delete(subscription)
        except Exception:
            self.chat_interface.send_message(
                user_id, f"You wasn't subscribed to {feed_url}!"
            )
            return
        self.chat_interface.send_message(
            user_id, f"You have been unsubscribed from {feed_url}!"
        )

    def list(self, message: entities.UserMessage):

        user_id = message.user_id

        subs = self.subscription_repo.fetch_by_user_id(user_id)
        if len(subs) == 0:
            self.chat_interface.send_message(user_id, "You have no subs!")
            return
        reply_msg = "Your subscriptions:\n"
        for sub in subs:
            reply_msg += f"- {sub.feed_url}\n"
        self.chat_interface.send_message(user_id, reply_msg)

    def send_helper(self, message: entities.UserMessage):
        helper = """Command available:
subscribe <feed> - subscribe to feed
unsubscribe <feed> - unsubscribe from feed
list - list your subscriptions
"""
        self.chat_interface.send_message(message.user_id, helper)

    def send_unauthorized(self, user_id: str):
        self.chat_interface.send_message(
            user_id, f"You ({user_id}) are not authorized to use this bot!"
        )

    def process(self, message: entities.UserMessage):
        if not self.allowlist.is_allowed(message.user_id):
            self.send_unauthorized(message.user_id)
            return

        functions = {
            "subscribe": self.subscribe,
            "unsubscribe": self.unsubscribe,
            "list": self.list,
        }

        command = message.text.split(" ")[0]
        if command not in functions:
            self.send_helper(message)
            return

        functions[command](message)
