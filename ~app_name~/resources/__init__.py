"""
    Loads the content from config files.

    Important: Do not import third party modules here. This module
    must work on its own without any other dependencies!
"""

import atexit
import importlib.resources
import json
import os
import tkinter.messagebox as tkmsg
from dataclasses import asdict, dataclass, field, fields
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import List, Optional

from const import (APP_VERSION, APPDATA, CONFIG_APPDATA, CONFIG_INFOS,
                   CONFIG_INFOS_DEFAULT, CONFIG_SETTINGS, CONFIG_USERS, LOGON)


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsRestrictions:
    """Dataclass for restrictive settings."""

    allow_all_users: bool
    allow_all_editors: bool
    allow_unsaved: bool
    allow_outside_workspace: bool
    strict_project: bool
    strict_machine: bool
    enable_information: bool


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsPaths:
    """Dataclass for paths (settings.json)."""

    catia: Path
    material: Path
    local_dependencies: Path
    release: Path


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsFiles:
    """Dataclass for files (settings.json)."""

    app: str
    launcher: str
    bounding_box_launcher: Optional[str]
    material: str
    workspace: str


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsUrls:
    """Dataclass for urls (settings.json)."""

    help: str | None


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsMails:
    """Dataclass for mails (settings.json)."""

    admin: str


@dataclass(slots=True, kw_only=True)
class Settings:  # pylint: disable=R0902
    """Dataclass for settings (settings.json)."""

    title: str
    debug: bool
    restrictions: SettingsRestrictions
    paths: SettingsPaths
    files: SettingsFiles
    urls: SettingsUrls
    mails: SettingsMails

    def __post_init__(self) -> None:
        self.restrictions = SettingsRestrictions(**dict(self.restrictions))  # type: ignore
        self.files = SettingsFiles(**dict(self.files))  # type: ignore
        self.paths = SettingsPaths(**dict(self.paths))  # type: ignore
        self.urls = SettingsUrls(**dict(self.urls))  # type: ignore
        self.mails = SettingsMails(**dict(self.mails))  # type: ignore


@dataclass(slots=True, kw_only=True, frozen=True)
class User:
    """Dataclass a user (users.json)."""

    logon: str
    id: str
    name: str
    mail: str

    @property
    def keys(self) -> List[str]:
        """Returns a list of all keys from the User dataclass."""
        return [f.name for f in fields(self)]

    @property
    def values(self) -> List[str]:
        """Returns a list of all values from the User dataclass."""
        return [getattr(self, f.name) for f in fields(self)]


@dataclass(slots=True, kw_only=True, frozen=True)
class Info:
    """Dataclass for an info messages (information.json)."""

    counter: int
    msg: str


@dataclass(slots=True, kw_only=True)
class AppData:
    """Dataclass for appdata settings."""

    version: str = field(default=APP_VERSION)
    counter: int = 0
    save_on_apply: bool = True

    def __post_init__(self) -> None:
        self.version = (
            APP_VERSION  # Always store the latest version in the appdata json
        )
        self.counter += 1


class Resources:  # pylint: disable=R0902
    """Class for handling resource files."""

    __slots__ = (
        "_settings",
        "_users",
        "_infos",
        "_appdata",
    )

    def __init__(self) -> None:
        self._read_settings()
        self._read_users()
        self._read_infos()
        self._read_appdata()

        atexit.register(self._write_appdata)

    @property
    def settings(self) -> Settings:
        """settings.json"""
        return self._settings

    @property
    def users(self) -> List[User]:
        """users.json"""
        return self._users

    @property
    def infos(self) -> List[Info]:
        """infos.json"""
        return self._infos

    @property
    def appdata(self) -> AppData:
        """Property for the appdata config file."""
        return self._appdata

    def _read_settings(self) -> None:
        """Reads the settings json from the resources folder."""
        with importlib.resources.open_binary("resources", CONFIG_SETTINGS) as f:
            self._settings = Settings(**json.load(f))

    def _read_users(self) -> None:
        """Reads the users json from the resources folder."""
        with importlib.resources.open_binary("resources", CONFIG_USERS) as f:
            self._users = [User(**i) for i in json.load(f)]


    def _read_infos(self) -> None:
        """Reads the information json from the resources folder."""
        infos_resource = (
            CONFIG_INFOS
            if importlib.resources.is_resource("resources", CONFIG_INFOS)
            else CONFIG_INFOS_DEFAULT
        )
        with importlib.resources.open_binary("resources", infos_resource) as f:
            self._infos = [Info(**i) for i in json.load(f)]

    def _read_appdata(self) -> None:
        """Reads the json config file from the appdata folder."""
        if os.path.exists(appdata_file := f"{APPDATA}\\{CONFIG_APPDATA}"):
            with open(appdata_file, "r", encoding="utf8") as f:
                try:
                    value = AppData(**json.load(f))
                except JSONDecodeError:
                    value = AppData()
                    tkmsg.showwarning(
                        title="Configuration warning",
                        message="The AppData config file has been corrupted. \
                            You may need to apply your preferences again.",
                    )
                self._appdata = value
        else:
            self._appdata = AppData()

    def _write_appdata(self) -> None:
        """Saves appdata config to file."""
        os.makedirs(APPDATA, exist_ok=True)
        with open(f"{APPDATA}\\{CONFIG_APPDATA}", "w", encoding="utf8") as f:
            json.dump(asdict(self._appdata), f)

    def get_user_by_logon(self, logon: Optional[str] = None) -> User:
        """
        Returns the user dataclass that matches the logon value. Returns the User of the current
        session if logon is omitted.

        Args:
            logon (Optional[str]): The user to fetch from the dataclass list.

        Raises:
            PytiaValueError: Raised when the user doesn't exist.

        Returns:
            User: The user from the dataclass list that matches the provided logon name.
        """
        if logon is None:
            logon = LOGON

        for index, value in enumerate(self._users):
            if value.logon == logon:
                return self._users[index]
        raise ValueError(f"The user {logon} does not exist.")

    def get_user_by_name(self, name: str) -> Optional[User]:
        """
        Returns the user dataclass that matches the name.

        Args:
            name (str): The username to fetch from the dataclass list.

        Returns:
            User: The user from the dataclass list that matches the provided name.
        """
        for index, value in enumerate(self._users):
            if value.name == name:
                return self._users[index]
        return None

    def logon_exists(self, logon: Optional[str] = None) -> bool:
        """
        Returns wether the users logon exists in the dataclass, or not. Uses the logon-value of the
        current session if logon is omitted.

        Args:
            logon (str): The logon name to search for.

        Returns:
            bool: The user from the dataclass list that matches the provided logon name.
        """
        if logon is None:
            logon = LOGON

        for user in self._users:
            if user.logon == logon:
                return True
        return False

    def get_info_msg_by_counter(self) -> List[str]:
        """
        Returns the info message by the app usage counter.

        Returns:
            List[str]: A list of all messages that should be shown at the counter value.
        """
        values = []
        for index, value in enumerate(self._infos):
            if value.counter == self._appdata.counter:
                values.append(self._infos[index].msg)
        return values


resource = Resources()
