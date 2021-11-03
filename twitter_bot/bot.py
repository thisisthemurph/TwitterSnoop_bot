import time
from typing import List
from datetime import datetime
from telegram.ext import Updater
from telegram.error import BadRequest

from api import db as dbapi
from api.handle import Handle
from properties import Properties
from constants import TELEGRAM_TOKEN, TW_SLEEP_TIMEOUT_SECONDS


def send_telegram_message(updater: Updater, chat_id: str, message: str) -> None:
    """
    Sends a message to the designated chat_id, nothing happens if the chat_id cannot be found

    Parameters:
        updater (telegram.ext.Updater): updater for sending messages using the Telegram API
        chat_id (str): the chat identifier
        message (str): the text body of the message
    """
    try:
        updater.bot.send_message(chat_id=chat_id, text=message)
    except BadRequest:
        # The chat_id cannot be found
        return None


def dispatch_telegram_messages(updater: Updater, handle: Handle, tweet_urls: List[str]) -> None:
    """
    Dispatches given tweet_url messages to the appropriate chat_id.

    Parameters:
        updater (telegram.ext.Updater): updater for sending messages using the Telegram API
        handle (Handle): a dict representing the handle
    """
    for url in tweet_urls:
        for watcher in handle.watchers:
            send_telegram_message(updater, watcher.chat_id, f"@{handle.name} has tweeted:\n\n{url}")


def process_tweets(updater: Updater, since: datetime) -> None:
    """
    Determines if there are any new tweets and dispatches the Telegram messages

    Parameters:
        updater (telegram.ext.Updater): updater for sending messages using the Telegram API
        since (datetime.datetime): tweets cannot be older than this
    """
    stored_handles: List[str] = dbapi.get_all_handle_names()
    for handle_name in stored_handles:
        try:
            handle: Handle = dbapi.get_handle(handle_name)
        except Exception:
            continue

        if handle.has_watchers:
            tweet_urls = handle.recent_tweets(since)
            dispatch_telegram_messages(updater, handle, tweet_urls)


def main():
    props = Properties()
    updater = Updater(TELEGRAM_TOKEN)

    while True:
        props.update_last_request(datetime.utcnow())
        process_tweets(updater, since=props.last_request)
        time.sleep(TW_SLEEP_TIMEOUT_SECONDS)


if __name__ == "__main__":
    main()
