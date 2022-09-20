"""
    Frames submodule for the main window.
"""

from tkinter import Tk, ttk


class Frames:
    """Frames class for the main window. Holds all ttk frames."""

    def __init__(self, root: Tk) -> None:
        self._frame_data = ttk.Labelframe(
            master=root, style="LabelFrames.TLabelframe", text="Data"
        )
        self._frame_data.grid(
            row=0, column=0, sticky="nsew", padx=(10, 10), pady=(10, 5)
        )
        self._frame_data.grid_columnconfigure(1, weight=1)
        self._frame_data.grid_rowconfigure(3, weight=1)

        self._frame_export = ttk.Labelframe(
            master=root, style="LabelFrames.TLabelframe", text="Export"
        )
        self._frame_export.grid(
            row=1, column=0, sticky="nsew", padx=(10, 10), pady=(5, 10)
        )
        self._frame_export.grid_columnconfigure(1, weight=1)

        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        self._frame_footer = ttk.Frame(master=root, height=30, style="Footer.TFrame")
        self._frame_footer.grid(row=2, column=0, sticky="swe", padx=10, pady=(5, 10))
        self._frame_footer.grid_columnconfigure(1, weight=1)

    @property
    def export_frame(self) -> ttk.Labelframe:
        return self._frame_export

    @property
    def data_frame(self) -> ttk.Labelframe:
        return self._frame_data

    @property
    def footer(self) -> ttk.Frame:
        return self._frame_footer
