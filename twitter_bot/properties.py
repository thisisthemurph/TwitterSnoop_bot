import json
from typing import Union
from datetime import datetime


class Properties:
    def __init__(self) -> None:
        self._load()

    def _load(self) -> None:
        """Loads the data from the properties file"""
        with open("./properties.json", "r", encoding="utf8") as prop_f:
            self._data = json.load(prop_f)

    def _save(self) -> None:
        """Saves the new version of the properties file"""
        with open("./properties.json", "w", encoding="utf8") as prop_f:
            prop_f.write(json.dumps(self._data, indent=2))

        self._load()

    @property
    def last_request(self) -> Union[datetime, None]:
        """The date the last request for tweets was made"""
        iso_datetime = self._data["last_request"]
        return datetime.fromisoformat(iso_datetime) if iso_datetime else None

    def update_last_request(self, date: datetime) -> None:
        """
        Update the last_request property to the given date value

        Parameters:
            date (datetime.datetime): the new date to be stored
        """
        self._data["last_request"] = date.isoformat()
        self._save()
