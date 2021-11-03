from typing import List
from datetime import datetime

from api.twitter_funcs import get_most_recent_tweet_urls
from constants import TW_MAX_FETCH_COUNT


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

    def recent_tweets(self, since: datetime, limit: int = TW_MAX_FETCH_COUNT):
        """
        Fetches the most recent tweets for the handle.

        Parameters:
            since (datetime): the maximum age of tweets to be fetched
            limit (int): the maximim number of tweets to be fetched prior to since filtering

        Returns:
            a list of URLs associated with recent tweets
        """
        return get_most_recent_tweet_urls(self.name, since, limit)


def handle_factory(handle: dict) -> Handle:
    """Handle dict to object."""
    __handle = Handle(handle["id"], handle["handle"], handle["createdAt"], handle["updatedAt"])

    for watcher in handle["watchers"]:
        __handle.add_watcher(
            Watcher(watcher["id"], watcher["chatID"], watcher["createdAt"], watcher["updatedAt"])
        )

    return __handle
