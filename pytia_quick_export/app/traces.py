"""
    Traces submodule for the app.
"""

import os

import validators
from helper.verifier import verify_user_input
from pytia.log import log

from app.layout import Layout
from app.state_setter import UISetter
from app.vars import Variables


class Traces:
    """The Traces class. Responsible for all variable traces in the main window."""

    def __init__(
        self, variables: Variables, state_setter: UISetter, layout: Layout
    ) -> None:
        """
        Inits the Traces class. Adds the main windows' variable traces.

        Args:
            vars (Variables): The main window's variables.
            state_setter (UISetter): The state setter of the main window.
        """
        self.vars = variables
        self.set_ui = state_setter
        self.layout = layout

        self._add_traces()
        log.info("Traces initialized.")

    def _add_traces(self) -> None:
        """Adds all traces."""
        self.vars.project.trace_add("write", self.trace_project)
        self.vars.condition.trace_add("write", self.trace_condition)
        self.vars.quantity.trace_add("write", self.trace_quantity)
        self.vars.mail.trace_add("write", self.trace_mail)
        self.vars.folder.trace_add("write", self.trace_folder)

    def trace_project(self, *_) -> None:
        """Project variable trace. Verifies the user input for setting the export button."""
        verify_user_input(variables=self.vars, layout=self.layout)

    def trace_condition(self, *_) -> None:
        """Condition variable trace. Verifies the user input for setting the export button."""
        verify_user_input(variables=self.vars, layout=self.layout)

    def trace_quantity(self, *_) -> None:
        """Quantity variable trace. Verifies the user input for setting the export button."""
        try:
            int(self.vars.quantity.get())
        except ValueError:
            self.vars.quantity.set("1")
        verify_user_input(variables=self.vars, layout=self.layout)

    def trace_mail(self, *_) -> None:
        """Mail variable trace. Verifies the user input for setting the export button."""
        self.layout.input_mail.configure(
            foreground="black" if validators.email(self.vars.mail.get()) else "red"  # type: ignore
        )
        verify_user_input(variables=self.vars, layout=self.layout)

    def trace_folder(self, *_) -> None:
        """Folder variable trace. Verifies the user input for setting the export button."""
        is_dir = bool(
            os.path.isdir(self.vars.folder.get())
            and os.path.isabs(self.vars.folder.get())
        )
        self.layout.input_folder.configure(foreground="black" if is_dir else "red")
        verify_user_input(variables=self.vars, layout=self.layout)
