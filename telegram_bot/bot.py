import twit
from typing import List
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import db_api
from constants import TELEGRAM_TOKEN
from db_api import Watcher, WatcherNotFoundError


updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    """The standard bot start command"""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Let's get started, use the /help command to learn more about how to use my features...",
    )


HELP_MESSAGE = """*Need help?* 🤖

I'm a bot for snooping on your favourite Twitter accounts\.

Want to receive a Telegram message when your favourite *Twitter* account tweets something new?

I can do that for you\!

Add me to a group chat and see the updates right there\!

See a list of my commands below:

/help \- shows you this help message
/watch \- watch specific Twitter accounts
/watching \- show a list of Twitter handles being watched
/unwatch \- stop watching a Twitter account 
/latest \- gets the latest tweet for the given account

*Add me to a group chat\.\.\.*

If you would like to use my features in your favourite group chats, simply add me as a participant and use my commands to get started\. Since I only respond to commands, I don’t need to be given admin privileges\.
"""


def help(update, context):
    """Display a standard help message."""
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=HELP_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2
    )


def watch(update, context):
    """
    Watch a given Twitter handle.

    Command format:
        /watch @twitterhandle
        /watch @twitterhandle @somotherhandle
    """
    handles_to_watch: List[str] = sorted(list({h.lower().replace("@", "") for h in context.args}))

    try:
        watcher = db_api.get_watcher(update.effective_chat.id)
    except WatcherNotFoundError:
        watcher = None
    #
    # Do the background stuff
    #

    success_handles = []
    failure_handles = []
    for handle in handles_to_watch:
        success: bool = watcher.watch(handle)

        if success:
            success_handles.append(handle)
        else:
            failure_handles.append(handle)

    #
    # Build the reply message
    #

    if len(handles_to_watch) == 0:
        message = f"Ensure your command follows the pattern:\n\n/watch @twitterhandle\n\nYou can also add multiple Twitter handles seperated by a space."

    elif len(handles_to_watch) == 1:
        if success_handles:
            message = f"You are now snooping on @{handles_to_watch[0]} 👀"
        else:
            message = f"Something has gone wrong on our end, we can't seem to snoop on @{handles_to_watch[0]} at the moment."

    else:
        message = ""
        if success_handles:
            message += f"You are now snooping on the watching Twitter handles:\n\n"
            message += "\n".join([f"- @{handle}" for handle in list(success_handles)])

        if failure_handles:
            message += (
                "\nWe've had some issues and we've been unable to watch the following handles:\n\n"
            )
            message += "\n".join([f"- @{handle}" for handle in list(failure_handles)])

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def unwatch(update, context):
    """
    Stop watching a given Twitter handle or all handles.

    Command format:
        /unwatch all
        /unwatch @twitterhandle
        /unwatch @twitterhandle @someotherhandle
    """
    handles_to_del: List[str] = sorted(list({h.lower().replace("@", "") for h in context.args}))

    try:
        watcher: Watcher = db_api.get_watcher(update.effective_chat.id)
    except WatcherNotFoundError:
        watcher = None

    delete_all_handles: bool = len(handles_to_del) == 1 and handles_to_del[0] == "all"
    if delete_all_handles:
        handles_to_del = watcher.handles

    #
    # Unwatch the handles
    #

    unwatched_handles = []
    errored_handles = []
    for handle in handles_to_del:
        if handle in watcher.handles:
            watcher.unwatch(handle)
            unwatched_handles.append(handle)
        else:
            errored_handles.append(handle)

    #
    # Build the reply message
    #

    if not handles_to_del:
        message = f"Ensure your command follows the pattern:\n\n/unwatch @twitterhandle\n\nYou can also add multiple Twitter handles seperated by a space."
    elif delete_all_handles:
        message = (
            f"You have unwatched all Twitter handles 😥\n\nAdd some more using the /watch command!"
        )
    elif len(handles_to_del) == 1:
        if unwatched_handles:
            message = f"You are no longer snooping on @{handles_to_del[0]}"
        else:
            message = (
                f"You aren't watching @{handles_to_del[0]}, are you sure you typed it correctly?"
            )
    else:
        message = ""
        if unwatched_handles:
            message += "You are no longer snooping on the folloing Twitter handles:\n\n"
            message += "\n".join([f"- {h}" for h in unwatched_handles])

        if errored_handles:
            message += "\n\nYou were not watching the following handles:\n\n"
            message += "\n".join([f"- {h}" for h in errored_handles])
            message += "\n\nAre you sure you typed them correctly?"

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def latest(update, context):
    """
    Send a message with the latest tweet from a given Twitter handle.

    Command format:
        /latest @twitterhandle
    """
    if not context.args or len(context.args) > 1:
        message = f"Ensure your command follows the pattern:\n\n/latest @twitterhandle"
    else:
        handle = context.args[0].lower().replace("@", "")
        tweet_url = twit.get_latest_tweet_url(handle)
        message = f"Here's the latest tweet from @{handle}:\n\n{tweet_url}"

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def watching(update, context):
    """Send a message detailing the Twitter handles being watched in the current chat"""
    try:
        watcher: Watcher = db_api.get_watcher(update.effective_chat.id)
    except WatcherNotFoundError:
        watcher = None

    # Build the reply message

    if not watcher:
        message = "There has been an issue retrieving your information 😬"
    elif watcher.handles:
        handle_list = "\n".join([f"- @{handle}" for handle in watcher.handles])
        message = "You are watching the following Twitter handles:\n\n" + handle_list
    else:
        message = (
            "You aren't watching any Twitter handles at the moment. "
            "Use the /watch cmmand followed by a handle to see their tweets whenever they post."
        )

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def main():
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", help)
    watch_handler = CommandHandler("watch", watch)
    unwatch_handler = CommandHandler("unwatch", unwatch)
    watching_handler = CommandHandler("watching", watching)
    latest_handler = CommandHandler("latest", latest)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(watch_handler)
    dispatcher.add_handler(unwatch_handler)
    dispatcher.add_handler(watching_handler)
    dispatcher.add_handler(latest_handler)

    updater.start_polling()


if __name__ == "__main__":
    main()
