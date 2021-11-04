import json
from typing import Union
from datetime import datetime
from pathlib import Path


class Properties:
    """A class for handling the properties."""

    def __init__(self, file_path: Union[Path, str] = "./properties.json") -> None:
        """
        Parameters:
            file_path (pathlib.Path | str): the path to the properties file - default = './properties.json'
        """
        self.file_path = Path(file_path)

        self._create_if_not_exist()
        self._load()

    def _create_if_not_exist(self):
        """Creates the properties JSON file if it does not already exist."""
        if not self.file_path.exists():
            with open(self.file_path, "w", encoding="utf8") as prop_f:
                prop_f.write(json.dumps({"last_request": datetime.utcnow().isoformat()}, indent=2))

    def _load(self) -> None:
        """Loads the data from the properties file."""
        with open("./properties.json", "r", encoding="utf8") as prop_f:
            self._data = json.load(prop_f)

    def _save(self) -> None:
        """Saves the new version of the properties file."""
        with open("./properties.json", "w", encoding="utf8") as prop_f:
            prop_f.write(json.dumps(self._data, indent=2))

        self._load()

    @property
    def last_request(self) -> Union[datetime, None]:
        """The date the last request for tweets was made or None if a timestamp isn't present."""
        iso_datetime = self._data["last_request"]
        return datetime.fromisoformat(iso_datetime) if iso_datetime else None

    def update_last_request(self, date: datetime) -> None:
        """
        Update the last_request property to the given date value.

        Parameters:
            date (datetime.datetime): the new date to be stored
        """
        self._data["last_request"] = date.isoformat()
        self._save()
