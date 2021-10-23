CREATE TABLE IF NOT EXISTS twitter_handles
(
    _id SERIAL PRIMARY KEY,
    handle text NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT twitter_handles_handle_key UNIQUE (handle)
);

CREATE TABLE IF NOT EXISTS watchers
(
    _id SERIAL PRIMARY KEY,
    chat_id text NOT NULL,
    updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT watchers_chat_id_key UNIQUE (chat_id)
);

CREATE TABLE IF NOT EXISTS watcher_handle_join
(
    _id  SERIAL PRIMARY KEY,
    watcher_id integer NOT NULL,
    handle_id integer NOT NULL
);