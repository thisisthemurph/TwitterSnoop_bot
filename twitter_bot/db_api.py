import requests

from constants import DB_API_HOST, DB_API_PORT


base_url = f"http://{DB_API_HOST}:{DB_API_PORT}"


def fetch_handles() -> None:
    """Returns a list of all handles in the database"""
    response = requests.get(f"{base_url}/handle")
    return response.json()


def fetch_handle_watchers(handle: str) -> dict:
    """
    Returns the watcher chat_ids associated with the given Twitter handle

    Parameters:
        handle (str): the Twitter handle to be searched for
    """
    response = requests.get(f"{base_url}/handle/{handle}/watchers")
    return response.json()
