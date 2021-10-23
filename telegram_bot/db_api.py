import requests
from constants import API_BASE

def watch_handle(handle: str, chat_id: str):
    """
    Assign the chat_id to watch the given handle

    Parameters:
        handle (str): the Twitter handle
        chat_id (str): the chat_id to watch the handle
    """
    try:
        response = requests.post(f"{API_BASE}/handle/{handle}/watch/{chat_id}")
        return response.json()
    except requests.ConnectionError:
        return None


def delete_watch(handle: str, chat_id: str):
    """
    Remove a relationship between a Twitter handle and Telegram chat ID

    Parameters:
        handle (str): the Twitter handle
        chat_id (str): the Telegram chat ID
    """
    response = requests.delete(f"{API_BASE}/handle/{handle}/watch/{chat_id}")
    return response.json()


def fetch_watched_handles(chat_id: str):
    """
    Fetch the Twitter handles being watched by the given chat_id

    Parameters:
        chat_id (str): the chat_id to be searched
    """
    try:
        response = requests.get(f"{API_BASE}/watcher/{chat_id}")
        return response.json()
    except requests.ConnectionError:
        return None
