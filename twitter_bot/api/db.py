import requests
from typing import List

from api.handle import Handle, handle_factory
from constants import DB_API_HOST, DB_API_PORT


base_url = f"http://{DB_API_HOST}:{DB_API_PORT}"


def get_all_handle_names() -> List[str]:
    """Returns a list of all handle name strings."""
    response = requests.get(f"{base_url}/handles").json()

    if response and response["success"]:
        return response["payload"]["handles"]
    elif response and not response["success"]:
        raise Exception(response["error"]["message"])
    else:
        raise Exception("Respons is None!")


def get_handle(handle: str) -> Handle:
    """Returns a dict representing a handle and the watchers associated with it."""
    response = requests.get(f"{base_url}/handle/{handle}").json()

    if response and response["success"]:
        return handle_factory(response["payload"])
    elif response and not response["success"]:
        raise Exception(response["error"]["message"])
    else:
        raise Exception("There has been an issue retrieving the handle.")


def get_watcher(chat_id: str) -> dict:
    """Returns a dict representing a watcher and the handles they are following."""
    response = requests.get(f"{base_url}/watcher/{chat_id}").json()

    if response and response["success"]:
        return response["payload"]
    elif response and not response["success"]:
        raise Exception(response["error"]["message"])
    else:
        raise Exception("There has been an issue retrieving the watcher.")
