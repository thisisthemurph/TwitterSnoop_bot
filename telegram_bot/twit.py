import tweepy as tw
from typing import Optional

from constants import (
    TW_ACCESS_TOKEN,
    TW_ACCESS_TOKEN_SECRET,
    TW_API_KEY,
    TW_API_KEY_SECRET,
)


auth = tw.OAuthHandler(TW_API_KEY, TW_API_KEY_SECRET)
auth.set_access_token(TW_ACCESS_TOKEN, TW_ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)


def get_latest_tweet_url(handle: str) -> Optional[str]:
    """
    Returns a URL for the most recent tweet for the given handle.

    Parameters:
        handle (str): the Twitter handle to be searched for

    Returns:
        A URL relating linking to the latest tweet for the given handle
    """
    try:
        result = api.user_timeline(id=handle, count=1)
    except tw.error.TweepError:
        return None

    tweet = result[0]
    return f"https://twitter.com/{handle}/status/{tweet.id_str}"
