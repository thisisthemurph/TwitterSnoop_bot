from typing import List, Optional
import requests

from constants import DB_API_HOST, DB_API_PORT


DB_API_BASE = f"http://{DB_API_HOST}:{DB_API_PORT}"


class HandleNotFoundError(Exception):
    pass


class WatcherNotFoundError(Exception):
    pass


class Watcher:
    """Represnts a watcher and their handles."""

    def __init__(self, chat_id: str, handles: List[str]):
        self.chat_id: str = chat_id
        self.handles: List[str] = handles

    def watch(self, handle: str) -> Optional[dict]:
        return watch_handle(handle, self.chat_id)

    def unwatch(self, handle: str) -> None:
        if handle not in self.handles:
            return

        unwatch_handle(handle, self.chat_id)
        self.handles.remove(handle)


def watch_handle(handle: str, chat_id: str) -> bool:
    """
    Assign the chat_id to watch the given handle.

    Parameters:
        handle (str): the Twitter handle
        chat_id (str): the chat_id to watch the handle

    Returns:
        True if the watch was a success, otherwise False
    """
    try:
        response = requests.post(f"{DB_API_BASE}/watcher/{chat_id}/watch/{handle}")
        return response.json()["success"]
    except requests.ConnectionError:
        return None


def unwatch_handle(handle: str, chat_id: str) -> dict:
    """
    Remove a relationship between a Twitter handle and Telegram chat ID

    Parameters:
        handle (str): the Twitter handle
        chat_id (str): the Telegram chat ID
    """
    response = requests.delete(f"{DB_API_BASE}/watcher/{chat_id}/unwatch/{handle}")
    return response.json()


def get_watcher(chat_id: str) -> Optional[dict]:
    """
    Fetch watcher assoiated with the given chat_id.

    Parameters:
        chat_id (str): the chat_id of the watcher to be returned
    """
    try:
        response = requests.get(f"{DB_API_BASE}/watcher/{chat_id}").json()
    except requests.ConnectionError:
        return None

    if not response or not response["success"]:
        raise WatcherNotFoundError(response["error"]["message"])

    payload = response["payload"]
    handles = [h["handle"] for h in payload["handles"]]

    return Watcher(payload["chatID"], handles)
