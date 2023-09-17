import json
from tkinter import Tk
from tkinter import messagebox as tkmsg
from tkinter import simpledialog

import requests
from app.state_setter import UISetter
from app.vars import Variables
from helper.lazy_loaders import LazyDocumentHelper
from helper.translators import translate_project, translate_property_value
from pytia.log import log
from resources import resource


class Rps:
    def __init__(
        self,
        main_ui: Tk,
        ui_setter: UISetter,
        doc_helper: LazyDocumentHelper,
        variables: Variables,
    ) -> None:
        self.main_ui = main_ui
        self.ui_setter = ui_setter
        self.doc_helper = doc_helper
        self.variables = variables

    @staticmethod
    def _make_url(api_url: str) -> str:
        return f"http://{resource.rps.ip}:{resource.rps.port}{api_url}"

    @classmethod
    def setup_personal_access_token(cls, root: Tk) -> None:
        """Sets up the personal access token for the RPS upload. Writes the token to
        the appdata config file.

        Args:
            root (Tk): The main app. Required for the prompt to be in front of the app.
        """
        pat = simpledialog.askstring(
            parent=root,
            title=resource.settings.title,
            prompt=(f"Enter your personal access token for {resource.rps.name}."),
        )
        resource.appdata.personal_access_token = pat or ""
        cls.test_login()

    @classmethod
    def remove_personal_access_token(cls) -> None:
        """Removes the personal access token from the appdata config file."""
        resource.appdata.personal_access_token = ""
        resource.write_appdata()
        tkmsg.showinfo(
            title=resource.settings.title,
            message=f"Removed personal access token for {resource.rps.name}.",
        )

    @classmethod
    def test_login(cls) -> None:
        """Tests the access token for the RPS system. Shows respective information."""
        pat = resource.appdata.personal_access_token

        try:
            response = requests.request(
                method=resource.rps.api.login.method,
                url=cls._make_url(resource.rps.api.login.url),
                headers={resource.rps.api.login.api_header: pat},
            )
            if response.status_code == 401:
                tkmsg.showwarning(
                    title=resource.settings.title,
                    message=(
                        f"Your personal access token for {resource.rps.name} is not valid. "
                        "Press F6 to setup your access token."
                    ),
                )
            elif response.status_code != 200:
                tkmsg.showerror(
                    title=resource.settings.title,
                    message=(
                        f"The server could not process the request:\n\n"
                        f"{str(response.text)}"
                    ),
                )
            else:
                try:
                    response_body = json.loads(response.text)
                    rps_username = response_body[
                        resource.rps.api.login.response_username_key
                    ]
                except Exception as e:
                    rps_username = "Unknown"

                tkmsg.showinfo(
                    title=resource.settings.title,
                    message=(
                        f"You are logged to {resource.rps.name} as {rps_username}."
                    ),
                )

        except Exception as e:
            tkmsg.showerror(
                title=resource.settings.title,
                message=(
                    f"Failed to establish a connection with {resource.rps.name}:\n\n"
                    f"{e}"
                ),
            )

    def _process_schema(self) -> str:
        """Processes the schema for the RPS upload. The schema is defined in the
        RPS config file.

        RPS schema keywords are:
         - %: The prefix for fixed text
         - $: The prefix for default or app specific properties
         - No prefix: The property name

        Returns:
            str: A valid json for the upload.
        """
        data = {}
        schema = resource.rps.api.bought.create.schema

        for key, value in schema.items():
            value = str(value)
            if value.startswith("%"):
                value = value[1:]
            else:
                value = translate_property_value(
                    value=value,
                    selected_quantity=self.variables.quantity.get(),
                    selected_condition=self.variables.condition.get(),
                    selected_project=translate_project(
                        project=self.variables.project, doc_helper=self.doc_helper
                    ),
                    doc_helper=self.doc_helper,
                )
            data[key] = value
        return json.dumps(data)

    def upload_bought_item(self) -> None:
        """Uploads the data to the rps system."""
        data = self._process_schema()

        try:
            response = requests.request(
                method=resource.rps.api.bought.create.method,
                url=self._make_url(resource.rps.api.bought.create.url),
                headers={
                    "Accept": "application/json",
                    resource.rps.api.login.api_header: resource.appdata.personal_access_token,
                },
                data=data,
            )
            if response.status_code == 401:
                tkmsg.showwarning(
                    title=resource.settings.title,
                    message=(
                        f"Your personal access token for {resource.rps.name} is not valid. "
                        "Press F6 to setup your access token."
                    ),
                )
            elif response.status_code != 200:
                tkmsg.showerror(
                    title=resource.settings.title,
                    message=(
                        f"The server could not process the request:\n\n"
                        f"{str(response.text)}"
                    ),
                )
            else:
                log.info(f"Upload successful: {data!r}")
                tkmsg.showinfo(
                    title=resource.settings.title, message="Upload successful."
                )
                if resource.settings.export.close_app_after:
                    self.main_ui.after(200, self.main_ui.destroy)

        except Exception as e:
            tkmsg.showerror(
                title=resource.settings.title,
                message=(
                    f"Failed to establish a connection with {resource.rps.name}:\n\n"
                    f"{e}"
                ),
            )

        self.ui_setter.normal()
