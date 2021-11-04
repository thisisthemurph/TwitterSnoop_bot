# TwitterSnoop_bot

> A Telegram bot for snooping on your favourite Titter accounts.

## Usage

The Telegram bot listens to a number of commands from the user and performs the appropriate action. The following is a list of commands and actions:

| Command   | Action                                                |
| --------- | ----------------------------------------------------- |
| /help     | Displats a help message to the user                   |
| /watch    | Allows the user to specify a Twitter handle to watch  |
| /watching | Details the Twitter handles being watched by the user |
| /unwatch  | Stops watching the specified Twitter handles          |
| /latest   | Retrieves the Tweet for the specified Twitter handle  |

## Topology

The bot has four main components; the databasd, the API, the Twitter bot (for fetching the latest tweets) and the Telegram bot.
