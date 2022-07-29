import asyncio
import datetime
import time

from telegramfeed import interfaces, repositories, services


class FeederService:
    def __init__(
        self,
        chat_interface: interfaces.ChatInterface,
        subscription_repo: repositories.SubscriptionRepo,
        feed_downloader_service: services.FeedDownloaderService,
        wait_time_in_seconds=60,
    ):
        self.chat_interface = chat_interface
        self.subscription_repo = subscription_repo
        self.feed_downloader_service = feed_downloader_service
        self.wait_time = wait_time_in_seconds

    async def start(self):
        print("FeederService is starting")
        self.request_to_stop = False
        while not self.request_to_stop:
            self.process_feeds()
            await asyncio.sleep(self.wait_time)

    def stop(self):
        self.request_to_stop = True

    def process_feeds(self):
        subscriptions = self.subscription_repo.fetch_all()
        for subscription in subscriptions:
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
            print("Error sending message: {}".format(e))
            print("entry: {}".format(entry))
