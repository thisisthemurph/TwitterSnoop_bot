import time
from typing import List
from datetime import datetime
from telegram.ext import Updater
from telegram.error import BadRequest

from handle import Handle
from properties import Properties
from twit import get_most_recent_tweet_urls
from api.db import get_all_handles, get_handle
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


def dispatch_telegram_messages(updater, handle: Handle, tweet_urls) -> None:
    """
    Dispatches given tweet_url messages to the appropriate chat_id.

    Parameters:
        updater (telegram.ext.Updater): updater for sending messages using the Telegram API
        handle (Handle): a dict representing the handle
    """
    for url in tweet_urls:
        for watcher in handle.watchers:
            send_telegram_message(updater, watcher.chat_id, f"@{handle.name} has tweeted:\n\n{url}")


def process_tweets(updater, since: datetime) -> None:
    """
    Determines if there are any new tweets and dispatches the Telegram messages

    Parameters:
        updater (telegram.ext.Updater): updater for sending messages using the Telegram API
        since (datetime.datetime): tweets cannot be older than this
    """
    stored_handles: List[str] = get_all_handles()
    for handle_name in stored_handles:
        handle: Handle = get_handle(handle_name)

        if handle.has_watchers:
            tweet_urls = get_most_recent_tweet_urls(handle.name, since)
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
