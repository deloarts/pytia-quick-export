"""
    The callbacks submodule for the main window.
"""

from tkinter import Tk

from pytia.log import log
from resources import resource

from app.layout import Layout
from app.state_setter import UISetter
from app.vars import Variables


class Callbacks:
    """The callbacks class for the main window."""

    def __init__(
        self,
        root: Tk,
        variables: Variables,
        layout: Layout,
        ui_setter: UISetter,
    ) -> None:
        """
        Initializes the callbacks class.

        Args:
            root (Tk): The main window of the app.
            variables (Variables): The variables of the main window.
            layout (Layout): The layout of the main window.
            ui_setter (UISetter): The ui setter instance of the main window.
        """
        self.root = root
        self.vars = variables
        self.layout = layout
        self.set_ui = ui_setter
        self.readonly = bool(
            not resource.logon_exists()
            and not resource.settings.restrictions.allow_all_users
        )

        self._bind_button_callbacks()
        self._bind_widget_callbacks()
        log.info("Callbacks initialized.")

    def _bind_button_callbacks(self) -> None:
        """Binds all callbacks to the main windows buttons."""
        self.layout.button_save.configure(command=self.on_btn_save)
        self.layout.button_abort.configure(command=self.on_btn_abort)

    def _bind_widget_callbacks(self) -> None:
        """Binds all callbacks to the main windows widgets."""


    def on_btn_save(self) -> None:
        """
        Event handler for the OK button. Verifies the user input and saves the changes to the
        documents properties.
        """
        log.info("Callback for button 'Save'.")
        

    def on_btn_abort(self) -> None:
        """Callback function for the abort button. Closes the app."""
        log.info("Callback for button 'Abort'.")
        self.root.withdraw()
        self.root.destroy()
