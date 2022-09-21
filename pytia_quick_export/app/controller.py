"""
    Controller submodule for the main window's flow.
"""

from tkinter import Tk
from tkinter import messagebox as tkmsg

from const import KEEP, LOGON
from helper.lazy_loaders import LazyDocumentHelper
from pytia.exceptions import PytiaPropertyNotFoundError
from pytia_ui_tools.handlers.workspace_handler import Workspace
from resources import resource

from app.layout import Layout
from app.state_setter import UISetter
from app.vars import Variables


class Controller:
    """The Controller class for the main window's flow."""

    def __init__(
        self,
        root: Tk,
        doc_helper: LazyDocumentHelper,
        layout: Layout,
        vars: Variables,
        ui_setter: UISetter,
        workspace: Workspace,
    ) -> None:
        """
        Inits the Controller class.

        Args:
            root (Tk): The main window object.
            doc_helper (LazyDocumentHelper): The document helper object.
            layout (Layout): The layout of the main window.
            vars (Variables): The variables of the main window.
            ui_setter (UISetter): The state setter for the main window.
            workspace (Workspace): The workspace object.
        """
        self.root = root
        self.doc_helper = doc_helper
        self.layout = layout
        self.vars = vars
        self.set_ui = ui_setter
        self.workspace = workspace

        self.activate_ui = True

    def run_all_controllers(self):
        """Runs all controllers: This is the setup routine for the app."""
        self._permission_controller()
        self._default_values_controller()

        if self.activate_ui:
            self.set_ui.normal()
        else:
            self.set_ui.disabled()

    def _permission_controller(self) -> None:
        """
        Runs the permission controller. Handles permissions set in the settings.json and in the
        workspace file.
        """
        # Check if the workspace is active
        if not self.workspace.elements.active:
            self.activate_ui = False
            tkmsg.showinfo(
                title=resource.settings.title,
                message=(
                    "This workspace is disabled. You cannot export the bill of material of this "
                    "document."
                ),
            )
            return

        # Check user config permission.
        if (
            not resource.logon_exists()
            and not resource.settings.restrictions.allow_all_users
        ):
            self.activate_ui = False
            tkmsg.showinfo(
                title=resource.settings.title,
                message=(
                    "You are not allowed to export the bill of material: Your logon "
                    f"name ({LOGON}) doesn't exist in the user configuration."
                ),
            )
            return

        # Check workspace permission.
        if (
            self.workspace.elements.editors
            and LOGON not in self.workspace.elements.editors
            and not resource.settings.restrictions.allow_all_editors
        ):
            self.activate_ui = False
            tkmsg.showinfo(
                title=resource.settings.title,
                message=(
                    "You are not allowed to export the bill of material: Your logon "
                    f"name ({LOGON}) doesn't exist in the workspace configuration."
                ),
            )
            return

    def _default_values_controller(self) -> None:
        """
        Run the default values controller. Applies the settings from the workspace settings file.
        """
        # Set project
        project_values = [KEEP]
        if self.workspace.elements.projects:
            project_values.extend(self.workspace.elements.projects)
        self.layout.input_project.configure(values=project_values)

        # Set condition (always 'New' if doc source is bought)
        if self.doc_helper.document.product.source == 2:  # Source: Bought
            self.layout.input_condition.configure(
                values=[resource.settings.condition.new.name]
            )
            self.layout.input_condition.current(0)
        else:
            self.layout.input_condition.configure(
                values=[
                    resource.settings.condition.new.name,
                    resource.settings.condition.mod.name,
                ]
            )

        # Set mail list
        if resource.settings.mails.export:
            if resource.settings.debug:
                self.layout.input_mail.configure(
                    values=[resource.settings.mails.export_debug]
                )
            else:
                self.layout.input_mail.configure(values=resource.settings.mails.export)
