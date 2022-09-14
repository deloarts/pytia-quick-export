"""
    Submodule for managing the state of the widgets.
    The UI is mainly managed by the 'source' of the document.
"""

import tkinter as tk

from pytia.log import log
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

    def normal(self) -> None:
        """Sets the UI to state 'normal'."""
        log.debug("Setting main UI to state 'normal'.")

        self.layout.button_save.configure(state=tk.NORMAL)

        self.root.update_idletasks()

    def disabled(self) -> None:
        """
        Sets the UI to state 'disabled'.
        """
        log.debug("Setting main UI to state 'disabled'.")

        self.layout.button_save.configure(state=tk.DISABLED)

        self.root.update_idletasks()
