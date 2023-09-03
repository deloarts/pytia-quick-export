import os
from tkinter import DISABLED, NORMAL
from tkinter import messagebox as tkmsg

import validators
from app.layout import Layout
from app.vars import Variables
from resources import resource


def verify_user_input_for_export(variables: Variables, layout: Layout) -> None:
    """
    Verifies the user input and sets the export button accordingly.

    Args:
        variables (Variables): The main UIs variables.
        layout (Layout): The layout of the main UI.
    """
    if all(
        [
            len(variables.project.get()) > 0,
            variables.condition.get()
            in [
                resource.settings.condition.new.name,
                resource.settings.condition.mod.name,
            ],
            int(variables.quantity.get()) > 0,
            any(
                [
                    validators.email(variables.mail.get()),  # type: ignore
                    bool(
                        os.path.isdir(variables.folder.get())
                        and os.path.isabs(variables.folder.get())
                    ),
                ]
            ),
        ]
    ):
        layout.button_export.configure(state=NORMAL)
    else:
        layout.button_export.configure(state=DISABLED)


def verify_user_input_for_upload(
    variables: Variables, layout: Layout, source: int
) -> None:
    """
    Verifies the user input and sets the upload button accordingly.

    Args:
        variables (Variables): The main UIs variables.
        layout (Layout): The layout of the main UI.
        source (int [0, 1, 2]): The source of the document.
    """
    if all(
        [
            resource.settings.export.enable_rps,
            len(variables.project.get()) > 0,
            variables.condition.get() == resource.settings.condition.new.name,
            int(variables.quantity.get()) > 0,
            source == 2,
        ]
    ):
        layout.button_upload.configure(state=NORMAL)
    else:
        layout.button_upload.configure(state=DISABLED)
