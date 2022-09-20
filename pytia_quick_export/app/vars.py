"""
    The variables submodule for the app.
"""

from dataclasses import dataclass
from tkinter import DoubleVar, StringVar, Tk


@dataclass(slots=True, kw_only=True)
class Variables:
    """Dataclass for the main windows variables."""

    project: StringVar
    condition: StringVar
    quantity: StringVar
    note: StringVar

    mail: StringVar
    folder: StringVar

    progress: DoubleVar

    def __init__(self, root: Tk) -> None:
        """
        Inits the variables.

        Args:
            root (Tk): The main window.
        """

        self.project = StringVar(master=root, name="project")
        self.condition = StringVar(master=root, name="condition")
        self.quantity = StringVar(master=root, name="quantity", value="0")
        self.note = StringVar(master=root, name="note")

        self.mail = StringVar(master=root, name="mail")
        self.folder = StringVar(master=root, name="folder")

        self.progress = DoubleVar(master=root, name="progress", value=0)
