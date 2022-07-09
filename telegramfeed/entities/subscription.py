import datetime


class Subscription:
    def __init__(self, user_id, feed_url, last_check=None):
        self.user_id = user_id
        self.feed_url = feed_url
        if last_check == None:
            last_check = datetime.datetime.utcnow()
        self.last_check = last_check
