from datetime import datetime
from typing import List
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import BadRequest
import time

from db_api import fetch_handles, fetch_handle_watchers
from twit import get_most_recent_tweet_urls
from constants import TELEGRAM_TOKEN, TW_SLEEP_TIMEOUT_SECONDS
from properties import Properties


def send_message(updater: Updater, chat_id: str, message: str) -> None:
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


def get_handles() -> List[str]:
    """Returns a list of all handles from the database"""
    result = fetch_handles()
    if result and result["success"]:
        return result["payload"]["handles"]

    return []


def get_chat_ids_for_handle(handle: str) -> List[str]:
    """
    Returns a list of chat_ids that watch the given handle from the database

    Parameters:
        handle (str): the Twitter handle

    Returns:
        A list of chat_ids associated with the Twitter handle
    """
    result = fetch_handle_watchers(handle)
    if result and result["success"]:
        return result["payload"]["watcher_chat_ids"]

    return []


def send_new_tweets(updater, props: Properties):
    """
    Determines if there are any new tweets and sends a message to the appropriate conversations

    Parameters:
        updater (telegram.ext.Updater): updater for sending messages using the Telegram API
        props (Properties): an object representing the properties of the bot
    """
    from_date = props.last_request
    props.update_last_request(datetime.utcnow())

    handles = get_handles()
    for handle in handles:
        tweet_urls = get_most_recent_tweet_urls(handle, from_date=from_date)
        print(tweet_urls)

        for url in tweet_urls:
            chat_ids = get_chat_ids_for_handle(handle)
            for chat_id in chat_ids:
                send_message(updater, chat_id, f"@{handle} has tweeted:\n\n" + url)


def main():
    props = Properties()
    updater = Updater(TELEGRAM_TOKEN)

    while True:
        send_new_tweets(updater, props)
        time.sleep(TW_SLEEP_TIMEOUT_SECONDS)


if __name__ == "__main__":
    main()
