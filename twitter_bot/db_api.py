import requests


def fetch_handles():
    """Returns a list of all handles in the database"""
    response = requests.get(f"http://localhost:5000/handle")
    return response.json()


def fetch_handle_watchers(handle: str):
    """
    Returns the watcher chat_ids associated with the given Twitter handle

    Parameters:
        handle (str): the Twitter handle to be searched for
    """
    response = requests.get(f"http://localhost:5000/handle/{handle}/watchers")
    return response.json()
