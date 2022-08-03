import datetime
import time

from telegramfeed import interfaces, repositories, services


class FeederService:
    def __init__(
        self,
        chat_interface: interfaces.ChatInterface,
        subscription_repo: repositories.SubscriptionRepo,
        feed_downloader_service: services.FeedDownloaderService,
    ):
        self.chat_interface = chat_interface
        self.subscription_repo = subscription_repo
        self.feed_downloader_service = feed_downloader_service

    def start(self):
        print("Processing feeds")
        self.process_feeds()

    def process_feeds(self):
        subscriptions = self.subscription_repo.fetch_all()
        for subscription in subscriptions:
            print(
                f"Processing subscription {subscription.feed_url} for user {subscription.user_id}"
            )
            self._manage_subscription(subscription)

    def _manage_subscription(self, subscription):
        feed_content = self.feed_downloader_service.download(subscription.feed_url)

        if "entries" not in feed_content.keys():
            return

        for entry in feed_content["entries"]:
            self._manage_entry(subscription, entry)

        self._subscription_update_check(subscription)

    def _subscription_update_check(self, subscription):
        subscription.last_check = datetime.datetime.now()
        self.subscription_repo.update(subscription)

    def _manage_entry(self, subscription, entry):
        updated_parsed = datetime.datetime.fromtimestamp(
            time.mktime(entry["updated_parsed"])
        )
        if subscription.last_check < updated_parsed:
            self.send_entry(subscription, entry)

    def send_entry(self, subscription, entry):
        try:
            self.chat_interface.send_message(subscription.user_id, entry["link"])
        except Exception as e:
            print(f"Error sending message: {e}")
