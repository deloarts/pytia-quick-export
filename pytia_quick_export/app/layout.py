"""
    The layout of the app.
"""
from tkinter import DISABLED, PhotoImage, Tk, ttk

from pytia_ui_tools.widgets.entries import NumberEntry
from pytia_ui_tools.widgets.texts import ScrolledText
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

        self.help_png = PhotoImage(data=resource.get_png("help.png"))

        # region PROJECT
        lbl_project = ttk.Label(
            frames.data_frame,
            text="Project",
            width=12,
        )
        lbl_project.grid(
            row=0,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y, 2),
            sticky="nsew",
        )
        self._combo_project = ttk.Combobox(
            frames.data_frame,
            values=[],
            textvariable=variables.project,
            state=DISABLED,
        )
        self._combo_project.grid(
            row=0,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=(Layout.MARGIN_Y, 2),
            ipadx=2,
            ipady=2,
            sticky="nsew",
            columnspan=3,
        )
        # endregion

        # region CONDITION
        lbl_condition = ttk.Label(
            frames.data_frame,
            text="Condition",
            width=12,
            # font=("Segoe UI", 9, "bold"),
        )
        lbl_condition.grid(
            row=1,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, 2),
            sticky="nsew",
        )
        self._combo_condition = ttk.Combobox(
            frames.data_frame,
            textvariable=variables.condition,
            state=DISABLED,
        )
        self._combo_condition.grid(
            row=1,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=(2, 2),
            ipadx=2,
            ipady=2,
            sticky="nsew",
            columnspan=3,
        )
        # endregion

        # region QUANTITY
        lbl_quantity = ttk.Label(
            frames.data_frame,
            text="Quantity",
            width=12,
            # font=("Segoe UI", 9, "bold"),
        )
        lbl_quantity.grid(
            row=2,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, 2),
            sticky="nsew",
        )
        self._entry_quantity = NumberEntry(
            frames.data_frame,
            string_var=variables.quantity,
            state=DISABLED,
        )
        self._entry_quantity.grid(
            row=2,
            column=1,
            padx=(5, 2),
            pady=(2, 2),
            ipadx=2,
            ipady=2,
            sticky="nsew",
        )
        self._btn_qty_increase = ttk.Button(
            frames.data_frame,
            text="+",
            width=4,
            state=DISABLED,
        )
        self._btn_qty_increase.grid(
            row=2,
            column=2,
            padx=(2, 2),
            pady=(1, 1),
            sticky="nsew",
        )
        self._btn_qty_decrease = ttk.Button(
            frames.data_frame,
            text="-",
            width=4,
            state=DISABLED,
        )
        self._btn_qty_decrease.grid(
            row=2,
            column=3,
            padx=(2, Layout.MARGIN_X),
            pady=(1, 1),
            sticky="nsew",
        )
        # endregion

        # region NOT
        lbl_note = ttk.Label(
            frames.data_frame,
            text="Note",
            width=12,
        )
        lbl_note.grid(
            row=3,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(6, 2),
            sticky="new",
        )
        self._input_note = ScrolledText(
            parent=frames.data_frame,
            textvariable=variables.note,
            state=DISABLED,
            height=3,
            font=("Segoe UI", 9),
        )
        self._input_note.grid(
            row=3,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=(2, Layout.MARGIN_Y),
            ipadx=2,
            ipady=2,
            sticky="nsew",
            columnspan=3,
        )
        self._lbl_help_note = ttk.Label(image=self.help_png)
        self._lbl_help_note.place(x=55, y=130)
        # endregion

        # region MAIL
        lbl_mail = ttk.Label(
            frames.export_frame,
            text="Mail Address",
            width=12,
            # font=("Segoe UI", 9, "bold"),
        )
        lbl_mail.grid(
            row=0,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y, 2),
            sticky="nsew",
        )
        self._combo_mail = ttk.Combobox(
            frames.export_frame,
            values=[],
            textvariable=variables.mail,
            state=DISABLED,
        )
        self._combo_mail.grid(
            row=0,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=(Layout.MARGIN_Y, 2),
            ipadx=2,
            ipady=2,
            sticky="nsew",
            columnspan=3,
        )
        # endregion

        # region FOLDER
        lbl_export_folder = ttk.Label(
            frames.export_frame, text="Export Folder", width=12
        )
        lbl_export_folder.grid(
            row=1,
            column=0,
            padx=(Layout.MARGIN_X, 2),
            pady=(2, Layout.MARGIN_Y),
            sticky="nsew",
        )

        self._entry_export_folder = ttk.Entry(
            frames.export_frame,
            textvariable=variables.folder,
            state=DISABLED,
        )
        self._entry_export_folder.grid(
            row=1,
            column=1,
            padx=(5, 2),
            pady=(2, Layout.MARGIN_Y),
            ipadx=2,
            ipady=2,
            sticky="nsew",
            columnspan=2,
        )

        self._btn_browse_export_folder = ttk.Button(
            frames.export_frame,
            text="...",
            width=4,
            state=DISABLED,
        )
        self._btn_browse_export_folder.grid(
            row=1,
            column=3,
            padx=(2, Layout.MARGIN_X),
            pady=(1, Layout.MARGIN_Y - 1),
            sticky="nsew",
        )
        # endregion

        # region FRAME Footer ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        lbl_info = ttk.Label(
            frames.footer,
            text="",
        )
        lbl_info.grid(
            row=0, column=0, padx=(0, 5), pady=0, ipadx=2, ipady=2, sticky="nsew"
        )

        self._btn_export = ttk.Button(
            frames.footer, text="Export", style="Footer.TButton", state=DISABLED
        )
        self._btn_export.grid(row=0, column=1, padx=(5, 2), pady=0, sticky="e")

        self._btn_abort = ttk.Button(frames.footer, text="Exit", style="Footer.TButton")
        self._btn_abort.grid(row=0, column=2, padx=(2, 0), pady=0, sticky="e")

    @property
    def input_project(self) -> ttk.Combobox:
        return self._combo_project

    @property
    def input_condition(self) -> ttk.Combobox:
        return self._combo_condition

    @property
    def input_quantity(self) -> NumberEntry:
        return self._entry_quantity

    @property
    def button_increase_qty(self) -> ttk.Button:
        return self._btn_qty_increase

    @property
    def button_decrease_qty(self) -> ttk.Button:
        return self._btn_qty_decrease

    @property
    def input_note(self) -> ScrolledText:
        return self._input_note

    @property
    def input_mail(self) -> ttk.Combobox:
        return self._combo_mail

    @property
    def input_folder(self) -> ttk.Entry:
        return self._entry_export_folder

    @property
    def button_browse_folder(self) -> ttk.Button:
        return self._btn_browse_export_folder

    @property
    def button_export(self) -> ttk.Button:
        return self._btn_export

    @property
    def button_abort(self) -> ttk.Button:
        return self._btn_abort

    @property
    def help_note(self) -> ttk.Label:
        return self._lbl_help_note
