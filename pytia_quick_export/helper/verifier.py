import os
from tkinter import DISABLED, NORMAL

import validators
from app.layout import Layout
from app.vars import Variables
from resources import resource


def verify_user_input(variables: Variables, layout: Layout) -> None:
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
