import tweepy as tw
from datetime import datetime
from typing import List

from constants import (
    TW_ACCESS_TOKEN,
    TW_ACCESS_TOKEN_SECRET,
    TW_API_KEY,
    TW_API_KEY_SECRET,
)


auth = tw.OAuthHandler(TW_API_KEY, TW_API_KEY_SECRET)
auth.set_access_token(TW_ACCESS_TOKEN, TW_ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)


def stndardise_datetime(ts: datetime) -> datetime:
    """Ensures datetime timestamps are standardised for comparison, preventing issues comparing naive and aware datetimes"""
    fmt: str = "%Y %d %m %H %M %S"
    return datetime.strptime(ts.strftime(fmt), fmt)


def get_most_recent_tweet_urls(handle: str, since: datetime, limit: int) -> List[str]:
    """
    Returns a list of recent tweets; max fetched is limit and then filtered on since

    Parameters:
        handle (str): the Twitter handle to be searched for
        since (datetime.datetime): the maximum age of tweets to be fetched
        limit (int): the maximum number of tweets to be fetched prior to since filtering

    Returns:
        a list of URLs associated with recent tweets
    """
    since = stndardise_datetime(since)

    try:
        results = api.user_timeline(screen_name=handle, count=limit)
    except tw.error.TweepError:
        results = []

    # Ensure tweets are recent enough and return list of URL strings
    tweets = filter(lambda tweet: stndardise_datetime(tweet.created_at) > since, results)
    return [f"https://twitter.com/{handle}/status/{tweet.id_str}" for tweet in tweets]
