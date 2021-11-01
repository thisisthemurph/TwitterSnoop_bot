from flask import Blueprint

import db
from db import HandleNotFoundError
from routes.format_response import format_response

handle_routes = Blueprint("handle_routes", __name__)


@handle_routes.route("/handles")
def get_all_handles():
    """Retrieve a list of Twitter handles."""
    handles = db.fetch_all_handles()
    return format_response({"handles": handles})


@handle_routes.route("/handle/<handle>")
def get_handle(handle: str):
    """Retrieve data relating to the given Twitter handle."""
    try:
        handle = db.fetch_handle(handle)
        response = format_response(handle)
    except HandleNotFoundError as e:
        response = format_response(error={"message": f"{e}"})

    return response


@handle_routes.route("/handle/<handle>", methods=["POST"])
def create_new_handle(handle: str):
    """Adds the given handle to the database."""
    success = db.add_handle(handle)
    value = {"handle": handle}

    if success:
        return format_response(value), 201
    else:
        return (
            format_response(
                value,
                error={"message": "There has been an issue creating the handle at this time."},
            ),
            500,
        )
