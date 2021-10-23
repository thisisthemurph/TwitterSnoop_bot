from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from typing import List

import twit
import db_api
from constants import TELEGRAM_TOKEN


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
    """Display a standard help message"""
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=HELP_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2
    )


def watch(update, context):
    """
    Watch a given Twitter handle

    Command format:
        /watch @twitterhandle
        /watch @twitterhandle @somotherhandle
    """
    handles: List[str] = sorted(list({h.lower().replace("@", "") for h in context.args}))

    #
    # Do the background stuff
    #

    # TODO: Determine if the handles are actual Twitter accounts

    handle_success = {}
    for handle in handles:
        result = db_api.watch_handle(handle, update.effective_chat.id)
        if result is None:
            handle_success[handle] = False
        else:
            handle_success[handle] = True

    #
    # Build the reply message
    #

    if len(handles) == 0:
        message = f"Ensure your command follows the pattern:\n\n/watch @twitterhandle\n\nYou can also add multiple Twitter handles seperated by a space"
    
    elif len(handles) == 1:
        if handle_success[handle]:
            message = f"You are now snooping on @{handles[0]} 👀"
        else:
            message = f"Something has gone wrong on our end, we can't seem to snoop on @{handles[0]} at the moment."

    else:
        success_handles = [handle for handle in handles if handle_success[handle]]
        failure_handles = [handle for handle in handles if not handle_success[handle]]

        message = ""
        if success_handles:
            message += f"You are now snooping on the watching Twitter handles:\n\n"
            message += "\n".join([f"- @{handle}" for handle in list(handles)])
        if failure_handles:
            message += "\nWe've had some issues and we've been unable to watch the following handles:\n\n"
            message += "\n".join([f"- @{handle}" for handle in list(handles)])

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def unwatch(update, context):
    """
    Stop watching a given Twitter handle or all handles

    Command format:
        /unwatch all
        /unwatch @twitterhandle
        /unwatch @twitterhandle @someotherhandle
    """
    handles: List[str] = sorted(list({h.lower().replace("@", "") for h in context.args}))

    # TODO: Implement checking that the user is actually watching the handles

    #
    # Get the current chat's watched handles
    #
        
    if len(handles) == 0:
        # No handles given to unfollow
        message = f"Ensure your command follows the pattern:\n\n/unwatch @twitterhandle\n\nYou can also add multiple Twitter handles seperated by a space."
    else:
        handles_watched_response = db_api.fetch_watched_handles(update.effective_chat.id)
        if handles_watched_response and handles_watched_response["success"]:
            handles_watched = handles_watched_response["payload"]
        else:
            handles_watched = None
            message = "There has been an issue determining your watch list, please try again later 😔"

        if handles_watched is not None:
            #
            # Do the background stuff
            #

            handle_results = {}
            for handle in handles:
                if handle in handles_watched:
                    db_api.delete_watch(handle, update.effective_chat.id)
                    handle_results[handle] = True
                else:
                    handle_results[handle] = False

            #
            # Build the reply message
            #

            dropped_handles = [f"- @{handle}" for handle, result in handle_results.items() if result]
            error_handles = [f"- @{handle}" for handle, result in handle_results.items() if not result]

            if len(handles) == 1 and handles[0] == "all":
                # Request to drop all handles
                message = f"You have unwatched all Twitter handles 😥\n\nAdd some more using the /watch command!"
            elif len(handles) == 1:
                # A single handle given to unfollow
                if dropped_handles:
                    message = f"You are no longer snooping on @{handles[0]}"
                else:
                    message = f"You aren't watching @{handles[0]}, are you sure you typed it correctly?"
            else:
                # Multiple handles to unfollow
                message = ""
                if dropped_handles:
                    message += "You are no longer snooping on the folloing Twitter handles:\n\n"
                    message += "\n".join(dropped_handles)

                if error_handles:
                    message += "\n\nYou are not watching the following handles:\n\n"
                    message += "\n".join(error_handles)
                    message += "\n\nAre you sure you typed them correctly?"

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def latest(update, context):
    """
    Send a message with the latest tweet from a given Twitter handle

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
    response = db_api.fetch_watched_handles(update.effective_chat.id)

    if response and response["success"]:
        handles = response["payload"]
        if handles:
            handle_list = "\n".join([f"- @{handle}" for handle in handles])
            message = "You are watching the following Twitter handles:\n\n" + handle_list
        else:
            message = (
                "You aren't watching any Twitter handles at the moment. "
                "Use the /watch cmmand followed by a handle to see their tweets whenever they post."
            )
    else:
        message = "⛔ There has been an issue retrieving this information, please try again..."

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
