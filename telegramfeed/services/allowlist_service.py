from typing import List


class AllowListService:
    def __init__(self, ids: List[str]):
        self.ids = ids

    def is_allowed(self, id: str) -> bool:
        return id in self.ids
