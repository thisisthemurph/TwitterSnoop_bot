import psycopg2
from typing import Union, List

from constants import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


DB_CREDENTIALS = {
    "host": DB_HOST,
    "name": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
}


class Postgres:
    def __init__(self, host: str, name: str, user: str, password: str):
        self.host = host
        self.name = name
        self.user = user
        self.password = password

    def __enter__(self):
        self.conn = psycopg2.connect(
            host=self.host, database=self.name, user=self.user, password=self.password
        )
        self.cur = self.conn.cursor()

        return self.conn, self.cur

    def __exit__(self, type, value, traceback):
        self.cur.close()
        self.conn.close()


def fetch_all_handles() -> List[str]:
    """Fetches all Twitter handles in the database"""
    with Postgres(**DB_CREDENTIALS) as (_, cur):
        cur.execute("SELECT handle FROM twitter_handles")
        rows = cur.fetchall()

    return [handle[0] for handle in rows]


def fetch_handle_watchers(handle: str) -> List[str]:
    """
    Returns a List of watchers for a given handle

    Parameters:
        handle (str): the Twitter handle to be searched
    """
    query = """SELECT DISTINCT chat_id
    FROM watchers as w
    JOIN watcher_handle_join as whj ON w._id = whj.watcher_id
    JOIN twitter_handles as h ON whj.handle_id = h._id
    WHERE h.handle = %s;"""

    with Postgres(**DB_CREDENTIALS) as (_, cur):
        cur.execute(query, (handle,))
        rows = cur.fetchall()

    return [chat_id[0] for chat_id in rows]


def fetch_watcher_handles(chat_id: str) -> List[str]:
    """
    Returns a list of watched handles for the given Telegram chat ID

    Parameters:
        chat_id (str): the Telegram chat_id to be searched
    """
    query = """SELECT handle
    FROM watchers as w
    JOIN watcher_handle_join as whj ON w._id = whj.watcher_id
    JOIN twitter_handles as h ON whj.handle_id = h._id
    WHERE w.chat_id = %s"""

    with Postgres(**DB_CREDENTIALS) as cur:
        cur.execute(query, (chat_id,))
        rows = cur.fetchall()

    return [handle[0] for handle in rows]


def handle_exists(handle: str) -> bool:
    """
    Determines if the given handle exists in the database

    Parameters:
        handle (str): the Twitter handle to be checked

    Returns:
        bool: True if the handle exists, otherwise False
    """
    query = "SELECT handle FROM twitter_handles WHERE handle = %s LIMIT 1"

    with Postgres(**DB_CREDENTIALS) as (_, cur):
        cur.execute(query, (handle,))
        result = cur.fetchone()

    return result is not None


def watcher_exists(chat_id: str) -> bool:
    """
    Determines if the given Telegram chat ID exists in the database

    Parameters:
        chat_id (str): the Telegram chat ID to be checked

    Returns:
        bool: True if the chat_id exists, otherwise False
    """
    with Postgres(**DB_CREDENTIALS) as (_, cur):
        cur.execute("SELECT chat_id FROM watchers WHERE chat_id = %s", (chat_id,))
        result = cur.fetchone()

    return result is not None


def add_handle(handle: str) -> None:
    """
    Add the given handle if it doesn't exist

    Parameters:
        handle (str): the new handle to be added to the database

    """
    if not handle_exists(handle):
        with Postgres(**DB_CREDENTIALS) as (conn, cur):
            cur.execute("INSERT INTO twitter_handles (handle) VALUES (%s)", (handle,))
            conn.commit()

        return handle_exists(handle)

    return True


def add_watcher(chat_id: str) -> None:
    """
    Add the given chat_id to the database as a watcher

    Parameters:
        chat_id (str): the ID for the Telegram chat to be added to the database
    """
    if not watcher_exists(chat_id):
        with Postgres(**DB_CREDENTIALS) as (conn, cur):
            cur.execute("INSERT INTO watchers (chat_id) VALUES (%s)", (chat_id,))
            conn.commit()

        return watcher_exists(chat_id)

    return True


def delete_watched(handle: str, chat_id: str) -> bool:
    """Delete a relationship between the Twitter handle and Telegram chat.

    Parameters:
        handle (str): the Twitter handle to be watched
        chat_id (str): The chat ID of the Telegram chat doing the watching

    """
    query = "DELETE FROM watcher_handle_join WHERE handle_id = %s AND watcher_id = %s"
    with Postgres(**DB_CREDENTIALS) as (conn, cur):
        # Get the ID of the given handle
        cur.execute("SELECT _id FROM twitter_handles WHERE handle = %s", (handle,))
        handle_id: int = cur.fetchone()[0]

        # Get the ID of the given watcher
        cur.execute("SELECT _id FROM watchers WHERE chat_id = %s", (chat_id,))
        watcher_id: int = cur.fetchone()[0]

        cur.execute(query, (handle_id, watcher_id))
        conn.commit()

    return True


def watch_handle(handle: str, chat_id: str) -> bool:
    """Create a relationship between a Twitter handle and a Telegram chat ID.
    If the handle or chat_id do not exist, they are created automatically.

    Parameters:
        handle (str): the Twitter handle to be watched
        chat_id (str): The chat ID of the Telegram chat doing the watching

    """
    # Add the handle and watcher if they are not already in the database
    add_handle(handle)
    add_watcher(chat_id)

    with Postgres(**DB_CREDENTIALS) as (conn, cur):
        # Get the ID of the given handle
        cur.execute("SELECT _id FROM twitter_handles WHERE handle = %s", (handle,))
        handle_id: int = cur.fetchone()[0]

        # Get the ID of the given watcher
        cur.execute("SELECT _id FROM watchers WHERE chat_id = %s", (chat_id,))
        watcher_id: int = cur.fetchone()[0]

        # Check if the reationship already exists
        cur.execute(
            "SELECT _id FROM watcher_handle_join WHERE handle_id = %s AND watcher_id = %s LIMIT 1",
            (handle_id, watcher_id),
        )

        result = cur.fetchone()
        if result is None:
            cur.execute(
                "INSERT INTO watcher_handle_join (handle_id, watcher_id) VALUES (%s, %s);",
                (handle_id, watcher_id),
            )
            conn.commit()

    return True
