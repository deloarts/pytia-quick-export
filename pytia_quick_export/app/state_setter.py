"""
    Submodule for managing the state of the widgets.
    The UI is mainly managed by the 'source' of the document.
"""

import tkinter as tk

from helper.outlook import get_outlook
from helper.verifier import verify_user_input
from pytia.log import log
from pytia_ui_tools.handlers.workspace_handler import Workspace
from resources import resource

from app.layout import Layout
from app.vars import Variables


class UISetter:
    """UI Setter class for the main window."""

    def __init__(
        self,
        root: tk.Tk,
        layout: Layout,
        variables: Variables,
        workspace: Workspace,
    ) -> None:
        """Inits the UI Setter class for the main window.

        Args:
            root (tk.Tk): The main window object.
            layout (Layout): The layout of the main window.
            variables (Variables): The variables of the main window.
        """ """"""
        self.root = root
        self.layout = layout
        self.vars = variables
        self.workspace = workspace

    def normal(self) -> None:
        """Sets the UI to state 'normal'."""
        log.debug("Setting main UI to state 'normal'.")

        self.layout.input_project.configure(
            state="readonly"
            if resource.settings.restrictions.strict_project
            and self.workspace.elements.projects
            else tk.NORMAL
        )
        self.layout.input_condition.configure(state="readonly")
        self.layout.input_quantity.configure(state=tk.NORMAL)
        self.layout.button_increase_qty.configure(state=tk.NORMAL)
        self.layout.button_decrease_qty.configure(state=tk.NORMAL)
        self.layout.input_note.state = tk.NORMAL

        if get_outlook() is not None:
            self.layout.input_mail.configure(state=tk.NORMAL)

        self.layout.input_folder.configure(state=tk.NORMAL)
        self.layout.button_browse_folder.configure(state=tk.NORMAL)
        self.layout.button_abort.configure(state=tk.NORMAL)

        verify_user_input(
            variables=self.vars, layout=self.layout
        )  # This sets the export button

        self.root.config(cursor="arrow")
        self.root.update_idletasks()

    def disabled(self) -> None:
        """Sets the UI to state 'disabled'."""
        log.debug("Setting main UI to state 'disabled'.")

        self.layout.input_project.configure(state=tk.DISABLED)
        self.layout.input_condition.configure(state=tk.DISABLED)
        self.layout.input_quantity.configure(state=tk.DISABLED)
        self.layout.button_increase_qty.configure(state=tk.DISABLED)
        self.layout.button_decrease_qty.configure(state=tk.DISABLED)
        self.layout.input_note.state = tk.DISABLED
        self.layout.input_mail.configure(state=tk.DISABLED)
        self.layout.input_folder.configure(state=tk.DISABLED)
        self.layout.button_browse_folder.configure(state=tk.DISABLED)
        self.layout.button_export.configure(state=tk.DISABLED)

        self.root.config(cursor="arrow")
        self.root.update_idletasks()

    def working(self) -> None:
        """
        Sets the UI to state 'working'. Same as 'disabled', but with the abort button also disabled.
        """
        self.disabled()
        self.layout.button_abort.configure(state=tk.DISABLED)
        self.root.config(cursor="wait")
        self.root.update_idletasks()
