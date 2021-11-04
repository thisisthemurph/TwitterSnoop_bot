# TwitterSnoop_bot Database API

> The API for interactions with the bot's data.

## Responses

All sucesful responses will have the following JSON format response. The success boolean will be set to true and, where appropriate, the payload will be set. The payload could be an array or an object.

```json
{
  "success": true,
  "payload": {}
}
```

A failed response will look like the following:

```json
{
  "success": false,
  "error": {
    "message": "This is an example error message."
  }
}
```

All following response objects are detailing the content of the payload.

### All handles

```vim
GET /handles
```

Returns all handle names in an array.

```json
["TwitterHandle1", "AnotherTwitterHandle", "this_vid"]
```

### Handle

```vim
GET /handle/<handle>
```

Retrieves a handle information associated with the given handle, including information on all the Telegram chats watching the specific handle.

```json
{
  "id": 1,
  "handle": "TwitterHandle1",
  "createdAt": "2019-02-23T04:02:04.051Z",
  "updatedAt": "2019-02-23T04:02:04.051Z",
  "watchers": [
    {
      "id": 1,
      "chatID": "786567",
      "createdAt": "2019-02-23T04:02:04.051Z",
      "updatedAt": "2019-02-23T04:02:04.051Z"
    },
    {
      "id": 4,
      "chatID": "564271",
      "createdAt": "2020-05-21T06:21:56.551Z",
      "updatedAt": "2020-05-21T06:21:56.551Z"
    }
  ]
}
```

```vim
POST /handle/<handle>
```

Creates a new handle, if it doesn't already exist and returns a string of the handle created.

```json
{
  "handle": "TwitterHandle1"
}
```

### Watcher

```vim
GET /watcher/<chat_id>
```

Fetches an object representing the watcher and the handles being watched.

```json
{
  "id": 1,
  "chatID": "786567",
  "createdAt": "2019-02-23T04:02:04.051Z",
  "updatedAt": "2019-02-23T04:02:04.051Z",
  "handles": [
    {
      "id": 1,
      "handle": "TwitterHandle1",
      "createdAt": "2019-02-23T04:02:04.051Z",
      "updatedAt": "2019-02-23T04:02:04.051Z"
    }
  ]
}
```

```vim
POST /watcher/<chat_id>/watch/<handle>
```

Create a relationship between the watcher and the handle.

No payload is present within the result.

```vim
POST /watcher/<chat_id>/unwatch/<handle>
```

Deletes the relationship between a watcher and a handle.

No payload is present within the result.
