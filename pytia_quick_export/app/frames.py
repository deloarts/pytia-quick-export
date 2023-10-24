"""
    Frames submodule for the main window.
"""

from tkinter import Tk

from ttkbootstrap import Frame
from ttkbootstrap import Labelframe


class Frames:
    """Frames class for the main window. Holds all ttk frames."""

    def __init__(self, root: Tk) -> None:
        self._frame_data = Labelframe(master=root, text="Data")
        self._frame_data.grid(
            row=0, column=0, sticky="nsew", padx=(10, 10), pady=(10, 5)
        )
        self._frame_data.grid_columnconfigure(1, weight=1)
        self._frame_data.grid_rowconfigure(3, weight=1)

        self._frame_export = Labelframe(master=root, text="Export")
        self._frame_export.grid(
            row=1, column=0, sticky="nsew", padx=(10, 10), pady=(5, 10)
        )
        self._frame_export.grid_columnconfigure(1, weight=1)

        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        self._frame_footer = Frame(master=root, height=30)
        self._frame_footer.grid(row=2, column=0, sticky="swe", padx=10, pady=(5, 10))
        self._frame_footer.grid_columnconfigure(1, weight=1)

    @property
    def export_frame(self) -> Labelframe:
        return self._frame_export

    @property
    def data_frame(self) -> Labelframe:
        return self._frame_data

    @property
    def footer(self) -> Frame:
        return self._frame_footer
