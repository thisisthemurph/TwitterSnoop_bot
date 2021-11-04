# TwitterSnoop_bot Twitter bot

This aspect of the Telegram bot handles periodically checking for relevant tweets by twotter users stored within the database.

The following is the general flow:

1. Use the `db_api` to obtain handles from the database
1. Fetch recent tweets associated with these handles using the `tweepy` library
1. The tweets are then sent to the user using their Telegram chai_ids
