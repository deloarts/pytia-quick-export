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

from const import (
    APP_VERSION,
    APPDATA,
    CONFIG_APPDATA,
    CONFIG_DOCKET,
    CONFIG_EXCEL,
    CONFIG_EXCEL_DEFAULT,
    CONFIG_KEYWORDS,
    CONFIG_PROPS,
    CONFIG_PROPS_DEFAULT,
    CONFIG_SETTINGS,
    CONFIG_USERS,
    LOGON,
)


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsRestrictions:
    """Dataclass for restrictive settings."""

    allow_all_users: bool
    allow_all_editors: bool
    allow_unsaved: bool
    allow_outside_workspace: bool
    strict_project: bool


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsExport:
    """Dataclass for export settings."""

    apply_username: bool
    lock_drawing_views: bool  # TODO: This isn't used yet


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsConditionNew:
    """Dataclass for conditions of type new (settings.json)."""

    name: str


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsConditionMod:
    """Dataclass for conditions of type modified (settings.json)."""

    name: str
    overwrite: dict


@dataclass(slots=True, kw_only=True)
class SettingsCondition:
    """Dataclass for conditions (settings.json)."""

    new: SettingsConditionNew
    mod: SettingsConditionMod

    def __post_init__(self) -> None:
        self.new = SettingsConditionNew(**dict(self.new))  # type: ignore
        self.mod = SettingsConditionMod(**dict(self.mod))  # type: ignore


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsPaths:
    """Dataclass for paths (settings.json)."""

    catia: Path
    local_dependencies: Path
    release: Path


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsFiles:
    """Dataclass for files (settings.json)."""

    app: str
    launcher: str
    workspace: str


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsUrls:
    """Dataclass for urls (settings.json)."""

    help: str | None


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsMails:
    """Dataclass for mails (settings.json)."""

    subject: str
    admin: str
    export: List[str] | None
    export_debug: str


@dataclass(slots=True, kw_only=True)
class Settings:  # pylint: disable=R0902
    """Dataclass for settings (settings.json)."""

    title: str
    debug: bool
    restrictions: SettingsRestrictions
    export: SettingsExport
    condition: SettingsCondition
    paths: SettingsPaths
    files: SettingsFiles
    urls: SettingsUrls
    mails: SettingsMails

    def __post_init__(self) -> None:
        self.restrictions = SettingsRestrictions(**dict(self.restrictions))  # type: ignore
        self.export = SettingsExport(**dict(self.export))  # type: ignore
        self.condition = SettingsCondition(**dict(self.condition))  # type: ignore
        self.files = SettingsFiles(**dict(self.files))  # type: ignore
        self.paths = SettingsPaths(**dict(self.paths))  # type: ignore
        self.urls = SettingsUrls(**dict(self.urls))  # type: ignore
        self.mails = SettingsMails(**dict(self.mails))  # type: ignore


@dataclass(slots=True, kw_only=True)
class KeywordElements:
    """Dataclass for keyword elements."""

    partnumber: str
    revision: str
    definition: str
    nomenclature: str
    source: str
    made: str
    bought: str
    unknown: str
    description: str
    number: str
    type: str
    part: str
    assembly: str
    quantity: str
    bom: str
    summary: str


@dataclass(slots=True, kw_only=True)
class Keywords:
    """Dataclass for language specific keywords."""

    en: KeywordElements
    de: KeywordElements

    def __post_init__(self) -> None:
        self.en = KeywordElements(**dict(self.en))  # type: ignore
        self.de = KeywordElements(**dict(self.de))  # type: ignore


@dataclass(slots=True, kw_only=True)
class EXCEL:
    """Excel dataclass."""

    header_row: int | None
    data_row: int
    header_items: List[str]
    font: str
    size: int
    header_color: str
    header_bg_color: str
    data_color_1: str
    data_bg_color_1: str
    data_color_2: str
    data_bg_color_2: str


@dataclass(slots=True, kw_only=True, frozen=True)
class Props:
    """Dataclass for properties on the part (properties.json)."""

    project: str
    machine: str
    creator: str
    modifier: str

    @property
    def keys(self) -> List[str]:
        """Returns a list of all keys from the Props dataclass."""
        return [f.name for f in fields(self)]

    @property
    def values(self) -> List[str]:
        """Returns a list of all values from the Props dataclass."""
        return [getattr(self, f.name) for f in fields(self)]


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

    def __init__(self) -> None:
        self._read_settings()
        self._read_users()
        self._read_keywords()
        self._read_excel()
        self._read_docket()
        self._read_props()
        self._read_appdata()

        atexit.register(self._write_appdata)

    @property
    def settings(self) -> Settings:
        """settings.json"""
        return self._settings

    @property
    def keywords(self) -> Keywords:
        """keywords.json"""
        return self._keywords

    @property
    def props(self) -> Props:
        """properties.json"""
        return self._props

    @property
    def excel(self) -> EXCEL:
        """excel.json"""
        return self._excel

    @property
    def users(self) -> List[User]:
        """users.json"""
        return self._users

    @property
    def docket(self) -> dict:
        """docket.json"""
        return self._docket

    @property
    def appdata(self) -> AppData:
        """Property for the appdata config file."""
        return self._appdata

    def get_png(self, name: str) -> bytes:
        """Returns a png resource by its name."""
        with importlib.resources.open_binary("resources", name) as f:
            return f.read()

    def _read_settings(self) -> None:
        """Reads the settings json from the resources folder."""
        with importlib.resources.open_binary("resources", CONFIG_SETTINGS) as f:
            self._settings = Settings(**json.load(f))

    def _read_keywords(self) -> None:
        """Reads the keywords json from the resources folder."""
        with importlib.resources.open_binary("resources", CONFIG_KEYWORDS) as f:
            self._keywords = Keywords(**json.load(f))

    def _read_users(self) -> None:
        """Reads the users json from the resources folder."""
        with importlib.resources.open_binary("resources", CONFIG_USERS) as f:
            self._users = [User(**i) for i in json.load(f)]

    def _read_docket(self) -> None:
        """Reads the docket json from the resources folder."""
        with importlib.resources.open_binary("resources", CONFIG_DOCKET) as f:
            self._docket = json.load(f)

    def _read_props(self) -> None:
        """Reads the props json from the resources folder."""
        props_resource = (
            CONFIG_PROPS
            if importlib.resources.is_resource("resources", CONFIG_PROPS)
            else CONFIG_PROPS_DEFAULT
        )
        with importlib.resources.open_binary("resources", props_resource) as f:
            self._props = Props(**json.load(f))

    def _read_excel(self) -> None:
        """Reads the excel json from the resources folder."""
        excel_resource = (
            CONFIG_EXCEL
            if importlib.resources.is_resource("resources", CONFIG_EXCEL)
            else CONFIG_EXCEL_DEFAULT
        )
        with importlib.resources.open_binary("resources", excel_resource) as f:
            self._excel = EXCEL(**json.load(f))

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


resource = Resources()
