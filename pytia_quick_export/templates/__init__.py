"""
    Templates submodule for the app.
    Provides template files from the templates-folder.
"""

import importlib.resources
import os
import zipfile
from pathlib import Path
from typing import Optional

from const import PYTIA_QUICK_EXPORT
from const import TEMP
from const import TEMP_TEMPLATES
from const import TEMPLATE_DOCKET
from const import TEMPLATE_MAIL
from pytia_ui_tools.utils.files import file_utility
from resources import resource


class Templates:
    """
    The Templates class.
    """

    def __init__(self) -> None:
        """
        Inits the class. Extracts the templates files from the zipped app and copies them into
        the temp-folder (TEMP\\pytia_bill_of_material\\templates\\). Deletes templates from the
        temp-folder at application exit.

        Warning: If the app mode is set to DEBUG, all templates will be used from the apps
        templates folder, not from the zipped app.
        """
        self.tempfolder = Path(TEMP, PYTIA_QUICK_EXPORT)
        self.temp_docket_path = Path(TEMP_TEMPLATES, TEMPLATE_DOCKET)
        self.temp_mail_path = Path(TEMP_TEMPLATES, TEMPLATE_MAIL)

        self._docket_path = None

        if not resource.settings.debug:
            self._make_tempfolder()
            self._extract()

        self._get_docket_path()
        self._get_mail_path()

    def _make_tempfolder(self) -> None:
        """Creates the temp-folder for the templates. Deletes existing templates."""
        if os.path.exists(self.temp_docket_path):
            os.remove(self.temp_docket_path)
        os.makedirs(self.tempfolder, exist_ok=True)

    def _extract(self) -> None:
        """Extracts the templates from the zipped app."""
        try:
            with zipfile.ZipFile(
                Path(resource.settings.paths.release, resource.settings.files.app), "r"
            ) as zfile:
                zfile.extract(
                    member=f"templates/{TEMPLATE_DOCKET}", path=self.tempfolder
                )
                zfile.extract(member=f"templates/{TEMPLATE_MAIL}", path=self.tempfolder)
            file_utility.add_delete(
                path=self.temp_docket_path, skip_silent=True, at_exit=True
            )
            file_utility.add_delete(
                path=self.temp_mail_path, skip_silent=True, at_exit=True
            )
        except:
            pass

    @property
    def docket_path(self) -> Optional[Path]:
        """The path to the docket template file."""
        return self._docket_path

    @property
    def mail_path(self) -> Optional[Path]:
        return self._mail_path

    def _get_docket_path(self) -> None:
        """Returns the path to the docket template. Depends on the apps mode."""
        if resource.settings.debug:
            if importlib.resources.is_resource("templates", TEMPLATE_DOCKET):
                with importlib.resources.path("templates", TEMPLATE_DOCKET) as p:
                    self._docket_path = p
            else:
                self._docket_path = None

        else:
            self._docket_path = (
                self.temp_docket_path if os.path.exists(self.temp_docket_path) else None
            )

    def _get_mail_path(self) -> None:
        if resource.settings.debug:
            if importlib.resources.is_resource("templates", TEMPLATE_MAIL):
                with importlib.resources.path("templates", TEMPLATE_MAIL) as p:
                    self._mail_path = p
            else:
                self._mail_path = None

        else:
            self._mail_path = (
                self.temp_mail_path if os.path.exists(self.temp_mail_path) else None
            )


templates = Templates()
