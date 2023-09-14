"""
    Traces submodule for the app.
"""

import os

import validators
from app.layout import Layout
from app.state_setter import UISetter
from app.vars import Variables
from helper.verifier import verify_user_input_for_export, verify_user_input_for_upload
from pytia.log import log
from ttkbootstrap import Style


class Traces:
    """The Traces class. Responsible for all variable traces in the main window."""

    def __init__(
        self,
        variables: Variables,
        state_setter: UISetter,
        layout: Layout,
        style: Style,
        source: int,
    ) -> None:
        """
        Inits the Traces class. Adds the main windows' variable traces.

        Args:
            vars (Variables): The main window's variables.
            state_setter (UISetter): The state setter of the main window.
            layout (Layout): The apps layout instance.
            style (Style): The ttkbootstrap style instance.
            source (int [0, 1, 2]): The source of the document.
        """
        self.vars = variables
        self.set_ui = state_setter
        self.layout = layout
        self.style = style
        self.source = source

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
        verify_user_input_for_export(variables=self.vars, layout=self.layout)
        verify_user_input_for_upload(
            variables=self.vars, layout=self.layout, source=self.source
        )

    def trace_condition(self, *_) -> None:
        """Condition variable trace. Verifies the user input for setting the export button."""
        verify_user_input_for_export(variables=self.vars, layout=self.layout)
        verify_user_input_for_upload(
            variables=self.vars, layout=self.layout, source=self.source
        )

    def trace_quantity(self, *_) -> None:
        """Quantity variable trace. Verifies the user input for setting the export button."""
        try:
            int(self.vars.quantity.get())
        except ValueError:
            self.vars.quantity.set("1")
        verify_user_input_for_export(variables=self.vars, layout=self.layout)
        verify_user_input_for_upload(
            variables=self.vars, layout=self.layout, source=self.source
        )

    def trace_mail(self, *_) -> None:
        """Mail variable trace. Verifies the user input for setting the export button."""
        self.layout.input_mail.configure(
            foreground=self.style.colors.fg if validators.email(self.vars.mail.get()) else self.style.colors.danger  # type: ignore
        )
        verify_user_input_for_export(variables=self.vars, layout=self.layout)

    def trace_folder(self, *_) -> None:
        """Folder variable trace. Verifies the user input for setting the export button."""
        is_dir = bool(
            os.path.isdir(self.vars.folder.get())
            and os.path.isabs(self.vars.folder.get())
        )
        self.layout.input_folder.configure(foreground=self.style.colors.fg if is_dir else self.style.colors.danger)  # type: ignore
        verify_user_input_for_export(variables=self.vars, layout=self.layout)
