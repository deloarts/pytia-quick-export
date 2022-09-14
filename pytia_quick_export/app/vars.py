"""
    The variables submodule for the app.
"""

from dataclasses import dataclass
from tkinter import StringVar, Tk


@dataclass(slots=True, kw_only=True)
class Variables:
    """Dataclass for the main windows variables."""

    project: StringVar
    machine: StringVar

    def __init__(self, root: Tk) -> None:
        """
        Inits the variables.

        Args:
            root (Tk): The main window.
        """

        self.project = StringVar(master=root, name="project")
        self.machine = StringVar(master=root, name="machine")
