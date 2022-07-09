class UserMessage:
    def __init__(self, user_id: str, text: str, update_id: int):
        self.user_id = user_id
        self.text = text
        self.update_id = update_id
