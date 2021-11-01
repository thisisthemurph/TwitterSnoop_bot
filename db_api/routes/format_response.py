from typing import Union


def format_response(payload: Union[dict, None] = None, error: Union[dict, None] = None) -> dict:
    """
    Formats the payload into a standardised response format.

    Parameters:
        payload (dict): the payload object to be sent with the response
        error (dict): the error object to be sent with the response

    Returns:
        dict: the newly formatted response object
    """
    response = {"success": True}

    if payload is not None:
        response["payload"] = payload

    if error is not None:
        response["success"] = False
        response["error"] = {"message": error["message"]}

    return response
