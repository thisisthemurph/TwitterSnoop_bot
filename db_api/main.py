from typing import Union
from flask import Flask, request, abort
from flask_restful import Api

import db
from constants import DB_API_HOST, DB_API_PORT


app = Flask("TwitterSnoop_DB_Api")
api = Api(app)


def format_response(payload: Union[dict, None] = None, error: Union[dict, None] = None) -> dict:
    """
    Formats the payload into a standard response format

    Parameters:
        payload (dict): the payload object to be sent with the response
        error (dict): the error object to be sent with the response

    Returns:
        the newly formatted response object
    """
    response = {"success": True}

    if payload is not None:
        response["payload"] = payload

    if error is not None:
        response["success"] = False
        response["error"] = {"message": error["message"]}

    return response


@app.route("/handle/<handle>/watch/<chat_id>", methods=["DELETE"])
def delete_watch(handle: str, chat_id: str):
    db.delete_watched(handle, chat_id)
    return format_response()


@app.route("/handle/<handle>/watch/<chat_id>", methods=["POST"])
def watch_handle(handle: str, chat_id: str):
    """
    The given chat_id watches the given handle

    Parameters:
        handle (str): the Twitter handle to be watched
        chat_id (str): the ID of the Telegram chat doing the watching
    """
    success = db.watch_handle(handle, chat_id)

    if success:
        return format_response(), 201
    else:
        return (
            format_response(
                None, error={"message": "It has not been possible to watch the handle"}
            ),
            500,
        )


@app.route("/handle/<handle>/watchers")
def get_handle_watchers(handle: str):
    """
    Retrieve Telegram chat_ids watching the given Twitter handle

    Parameters:
        handle (str): the Twitter handle to be searched
    """
    watcher_ids = db.fetch_handle_watchers(handle)
    return format_response({"handle": handle, "watcher_chat_ids": watcher_ids})


@app.route("/handle/<handle>/exists")
def handle_exists(handle: str):
    """
    Determine if the given Twitter handle is in the database

    Parameters:
        handle (str): the Twitter handle to be determined
    """
    handle_exists = db.handle_exists(handle)
    return format_response({"handle": handle, "handleExists": handle_exists})


@app.route("/watcher/<chat_id>/exists")
def watcher_exists(chat_id: str):
    """
    Determine if the given Telegram chat ID is in the database

    Parameters:
        chat_id (str): the Twitter handle to be determined
    """
    watcher_exists = db.watcher_exists(chat_id)
    return format_response({"chatId": chat_id, "chatIdExists": watcher_exists})


@app.route("/watcher/<chat_id>")
def get_watcher_handles(chat_id: str):
    """
    Retrieve the handles being watched by the given Telegram chat ID

    Parameters:
        chat_id (str): the Telegram chat ID to be searched
    """
    handles = db.fetch_watcher_handles(chat_id)
    return format_response(handles)


@app.route("/handle/<handle>", methods=["POST"])
def create_new_handle(handle):
    """
    Adds the given handle to the database

    Parameters:
        handle (str): the new handle to be added
    """
    success = db.add_handle(handle)
    value = {"handle": handle}

    if success:
        return format_response(value), 201
    else:
        return format_response(value, error={"message": "The handle was not created"}), 500


@app.route("/handle")
def get_all_handles():
    """Retrieved all current Twitter handles stored in the database"""
    handles = db.fetch_all_handles()
    return format_response({"handles": handles})


if __name__ == "__main__":
    app.run(host=DB_API_HOST, port=DB_API_PORT)
