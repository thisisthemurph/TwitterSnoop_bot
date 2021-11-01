from flask import Blueprint

import db
from db import (
    WatcherNotFoundError,
    NoWatchRelationshipExistsError,
    HandleNotFoundError,
    WatchRelationshipAlreadyExistsError,
)
from routes.format_response import format_response

watcher_routes = Blueprint("watcher_routes", __name__)


@watcher_routes.route("/watcher/<chat_id>")
def get_watcher(chat_id: str):
    """Fetches an object representing the watcher and the handles being watched."""
    try:
        watcher = db.fetch_watcher(chat_id)
        response = format_response(watcher)
    except WatcherNotFoundError as e:
        response = format_response(error={"message": f"{e}"})

    return response


@watcher_routes.route("/watcher/<chat_id>/watch/<handle>", methods=["POST"])
def watch_handle(handle: str, chat_id: str):
    """Create a relationship between the watcher and the handle."""
    try:
        success = db.create_watch_relationship(handle, chat_id)

        if success:
            return format_response(), 201
        else:
            err = {"message": f"There has been an issue tryin to watch @{handle} at his time."}
            return format_response(error=err), 500

    except WatchRelationshipAlreadyExistsError as e:
        err = {"message": f"The handle @{handle} is already being watched."}
        return format_response(error=err), 409


@watcher_routes.route("/watcher/<chat_id>/unwatch/<handle>", methods=["DELETE"])
def unwatch_handle(handle: str, chat_id: str):
    """Deletes the relationship between a watcher and a handle."""
    try:
        db.delete_watch_relationship(handle, chat_id)
    except HandleNotFoundError as e:
        return format_response(error={"message": f"{e}"}), 404
    except WatcherNotFoundError as e:
        return format_response(error={"message": f"{e}"}), 404
    except NoWatchRelationshipExistsError as e:
        return format_response(error={"message": f"{e}"}), 404

    return format_response()
