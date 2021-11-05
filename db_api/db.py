import psycopg2
from typing import List

from constants import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

DB_CREDENTIALS = {
    "host": DB_HOST,
    "name": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
}


class WatcherNotFoundError(Exception):
    pass


class HandleNotFoundError(Exception):
    pass


class NoWatchRelationshipExistsError(Exception):
    pass


class WatchRelationshipAlreadyExistsError(Exception):
    pass


def assert_handle_exists(handle: str) -> None:
    """Raises HandelNotFoundError if the handle does not exist."""
    if not handle_exists(handle):
        raise HandleNotFoundError(f"The @{handle} Twitter handle could not be found.")


def assert_watcher_exists(chat_id: str):
    """Raises a WatcherNotFoundError if a watcher with the given chat_id does not exist."""
    if not watcher_exists(chat_id):
        raise WatcherNotFoundError(f"A watcher with chat_id {chat_id} could not be found.")


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
    """Fetches a list of Twitter handles."""
    with Postgres(**DB_CREDENTIALS) as (_, cur):
        cur.execute("SELECT handle FROM twitter_handles;")
        rows = cur.fetchall()

    return [handle[0] for handle in rows]


def fetch_handle(handle: str):
    """
    Fetches data relating to the given handle.

    Parameters:
        handle (str): the Twitter handle to be fetched.

    Returns:
        a dictionary representing a Twitter handle and it's watchers
    """
    assert_handle_exists(handle)

    query = """SELECT th._id, th.handle, th.created_at, th.updated_at,
               w._id, w.chat_id, w.created_at, w.updated_at
               FROM twitter_handles th
               LEFT JOIN watcher_handle_join whj ON th._id = whj.handle_id
               LEFT JOIN watchers w ON whj.watcher_id = w._id
               WHERE th.handle = %s;"""

    with Postgres(**DB_CREDENTIALS) as (_, cur):
        cur.execute(query, (handle,))
        rows = cur.fetchall()

    handle = {
        "id": rows[0][0],
        "handle": rows[0][1],
        "createdAt": rows[0][2],
        "updatedAt": rows[0][3],
        "watchers": [],
    }

    for row in rows:
        if row[4]:
            handle["watchers"].append(
                {
                    "id": row[4],
                    "chatID": row[5],
                    "createdAt": row[6],
                    "updatedAt": row[7],
                }
            )

    return handle


def fetch_watcher(chat_id: str) -> dict:
    """
    Fetches watcher data relating to the given chat_id.

    Parameters:
        chat_id (str): the chat_id of the watcher to be returned

    Returns:
        a dict representation of a watcher and the handles being watched
    """
    assert_watcher_exists(chat_id)

    query = """SELECT th._id, th.handle, th.created_at, th.updated_at, 
               w._id, w.chat_id, w.created_at, w.updated_at
               FROM watchers w
               LEFT JOIN watcher_handle_join whj ON w._id = whj.watcher_id
               LEFT JOIN twitter_handles th ON whj.handle_id = th._id
               WHERE w.chat_id = %s;"""

    with Postgres(**DB_CREDENTIALS) as (_, cur):
        cur.execute(query, (chat_id,))
        rows = cur.fetchall()

    watcher = {
        "id": rows[0][4],
        "chatID": rows[0][5],
        "createdAt": rows[0][6],
        "updatedAt": rows[0][7],
        "handles": [],
    }

    for row in rows:
        if row[0]:
            watcher["handles"].append(
                {
                    "id": row[0],
                    "handle": row[1],
                    "createdAt": row[2],
                    "updatedAt": row[3],
                }
            )

    return watcher


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


def add_handle(handle: str) -> bool:
    """
    Add the given handle if it doesn't already exist.

    Parameters:
        handle (str): the new handle to be added to the database

    Returns:
        a boolean representing success or failure
    """
    if handle_exists(handle):
        return True

    with Postgres(**DB_CREDENTIALS) as (conn, cur):
        cur.execute("INSERT INTO twitter_handles (handle) VALUES (%s)", (handle,))
        conn.commit()

    return handle_exists(handle)


def add_watcher(chat_id: str) -> bool:
    """
    Add the given watcher chat_id to the database.

    Parameters:
        chat_id (str): the ID for the Telegram chat to be added to the database

    Returns:
        a boolean representing success or failure
    """
    if watcher_exists(chat_id):
        return True

    with Postgres(**DB_CREDENTIALS) as (conn, cur):
        cur.execute("INSERT INTO watchers (chat_id) VALUES (%s)", (chat_id,))
        conn.commit()

    return watcher_exists(chat_id)


def delete_watch_relationship(handle: str, chat_id: str):
    """
    Delete a relationship between the Twitter handle and Telegram chat.

    Parameters:
        handle (str): the Twitter handle to be watched
        chat_id (str): The chat ID of the Telegram chat doing the watching

    Returns:
        a boolean representing success or failure
    """
    assert_handle_exists(handle)
    assert_watcher_exists(chat_id)

    watcher = fetch_watcher(chat_id)
    watched_handles = [h["handle"] for h in watcher["handles"]]
    if not handle in watched_handles:
        raise NoWatchRelationshipExistsError(
            f"The handle @{handle} is not being watched by {chat_id}."
        )

    handle = fetch_handle(handle)

    query = "DELETE FROM watcher_handle_join WHERE handle_id = %s AND watcher_id = %s;"
    with Postgres(**DB_CREDENTIALS) as (conn, cur):
        cur.execute(query, (handle["id"], watcher["id"]))
        conn.commit()


def create_watch_relationship(_handle: str, _chat_id: str) -> bool:
    """
    Create a relationship between a Twitter handle and a Telegram chat ID.
    If the handle or chat_id do not exist, they are created automatically.

    Parameters:
        handle (str): the Twitter handle to be watched
        chat_id (str): The chat ID of the Telegram chat doing the watching

    Returns:
        a boolean representing success or failure
    """
    # Add the handle and watcher if they are not already in the database
    add_handle(_handle)
    add_watcher(_chat_id)

    # Determine if the watcher is already watching the handle and exit if so
    watcher = fetch_watcher(_chat_id)
    watcher_watched_handles = [h["handle"] for h in watcher["handles"]]
    if _handle in watcher_watched_handles:
        raise WatchRelationshipAlreadyExistsError()

    handle = fetch_handle(_handle)

    # Create the new relationship
    query = "INSERT INTO watcher_handle_join (handle_id, watcher_id) VALUES (%s, %s);"
    with Postgres(**DB_CREDENTIALS) as (conn, cur):
        cur.execute(query, (handle["id"], watcher["id"]))
        conn.commit()

    return True
