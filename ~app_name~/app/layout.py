"""
    The layout of the app.
"""
from tkinter import DISABLED, WORD, Tk, ttk

from resources import resource

from app.frames import Frames
from app.vars import Variables


class Layout:
    """The layout class of the app, holds all widgets."""

    MARGIN_X = 10
    MARGIN_Y = 10

    def __init__(self, root: Tk, frames: Frames, variables: Variables) -> None:
        """
        Inits the Layout class. Creates and places the widgets of the main window.

        Args:
            root (Tk): The main window.
            frames (Frames): The frames of the main window.
            variables (Variables): The variables of the main window.
        """
        lbl_my_label = ttk.Label(
            frames.my_frame,
            text="Partnumber",
            width=12,
            font=("Segoe UI", 9, "bold"),
        )
        lbl_my_label.grid(
            row=0,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y, 2),
            sticky="nsew",
        )


        # region FRAME Footer ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        lbl_info = ttk.Label(
            frames.footer,
            text="",
        )
        lbl_info.grid(
            row=0, column=0, padx=(0, 5), pady=0, ipadx=2, ipady=2, sticky="nsew"
        )

        self._btn_save = ttk.Button(
            frames.footer, text="Save", style="Footer.TButton", state=DISABLED
        )
        self._btn_save.grid(row=0, column=1, padx=(5, 2), pady=0, sticky="e")

        self._btn_abort = ttk.Button(
            frames.footer, text="Abort", style="Footer.TButton"
        )
        self._btn_abort.grid(row=0, column=2, padx=(2, 0), pady=0, sticky="e")


    @property
    def button_save(self) -> ttk.Button:
        """Returns the save button."""
        return self._btn_save

    @property
    def button_abort(self) -> ttk.Button:
        """Returns the abort button."""
        return self._btn_abort
