from telegramfeed.newsfeed import NewsFeed
from telegramfeed.telegram import Telegram


class TelegramFeed:
    def __init__(
        self,
        blogfeed: NewsFeed,
        telegram: Telegram,
    ):
        self.blogfeed = blogfeed
        self.telegram = telegram

    def take_subs_fetch_rss_send(self):
        pass
        # counter = 0

        # for article in self.blogfeed.articles(blog):
        #     if self.article_repository.alredy_saved(article.url):
        #         continue

        #     try:
        #         message = f"New article from {article.blog}!\n"
        #         message += f"[{article.title}]({article.url})"
        #         self.telegram.send_message(message)
        #         print(f"Sent message: {article.blog} - {article.title}")
        #     except Exception as e:
        #         print("Error sending message", e)
        #         print(message)
        #         continue
        #     else:
        #         self.article_repository.save(article)
        #         counter += 1

        # print(f"Sent {counter} articles")
