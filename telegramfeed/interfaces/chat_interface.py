from abc import ABC, abstractmethod
from typing import Optional

from telegramfeed import entities


class ChatInterface(ABC):
    @abstractmethod
    def send_message(self, user: str, message: str):
        pass  # pragma: no cover

    @abstractmethod
    def fetch_message(self, offset: int = 0) -> Optional[entities.UserMessage]:
        pass  # pragma: no cover
