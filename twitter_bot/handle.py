from typing import List
from datetime import datetime


class Watcher:
    def __init__(self, id: int, chat_id: str, created_at: datetime, updated_at: datetime):
        self._id: int = id
        self.chat_id: str = chat_id
        self.created_at: datetime = created_at
        self.updated_at: datetime = updated_at


class Handle:
    def __init__(self, id: int, name: str, created_at: datetime, updated_at: datetime):
        self._id: int = id
        self.name: str = name
        self.created_at: datetime = created_at
        self.updated_at: datetime = updated_at

        self.watchers: List[Watcher] = []

    def add_watcher(self, watcher: Watcher) -> None:
        """Adds a Watcher to the watchers list"""
        self.watchers.append(watcher)

    @property
    def has_watchers(self) -> bool:
        """Returns True if the Handle has watchers, otherwise False"""
        return self.watchers


def handle_factory(handle: dict) -> Handle:
    """Handle dict to object."""
    __handle = Handle(handle["id"], handle["handle"], handle["createdAt"], handle["updatedAt"])

    for watcher in handle["watchers"]:
        __handle.add_watcher(
            Watcher(watcher["id"], watcher["chatID"], watcher["createdAt"], watcher["updatedAt"])
        )

    return __handle
