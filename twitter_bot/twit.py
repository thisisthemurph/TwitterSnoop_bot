from typing import Union, List
import tweepy as tw
from datetime import datetime

from constants import (
    TW_ACCESS_TOKEN,
    TW_ACCESS_TOKEN_SECRET,
    TW_API_KEY,
    TW_API_KEY_SECRET,
    TW_MAX_FETCH_COUNT,
)


auth = tw.OAuthHandler(TW_API_KEY, TW_API_KEY_SECRET)
auth.set_access_token(TW_ACCESS_TOKEN, TW_ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)


def get_most_recent_tweet_urls(handle: str, from_date: datetime) -> List[str]:
    """
    Returns a URL for the most recent tweets for the given handle from the given from_date

    Parameters:
        handle (str): the Twitter handle to be searched for
        from_date (datetime.datetime): tweets cannot be older than this date

    Returns:
        A list of URLs associated with recent tweets
    """
    try:
        results = api.user_timeline(id=handle, count=TW_MAX_FETCH_COUNT)
    except tw.error.TweepError:
        results = None

    urls = []
    if results:
        for tweet in results:
            print(f"{tweet.created_at} > {from_date} = {tweet.created_at > from_date}")
            if tweet.created_at > from_date:
                urls.append(f"https://twitter.com/{handle}/status/{tweet.id_str}")

    return urls
