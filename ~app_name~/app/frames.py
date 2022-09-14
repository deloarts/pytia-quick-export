"""
    Frames submodule for the main window.
"""

from tkinter import Tk, ttk


class Frames:
    """Frames class for the main window. Holds all ttk frames."""

    def __init__(self, root: Tk) -> None:
        self._my_frame = ttk.Labelframe(
            master=root, style="Left.TLabelframe", text="Infrastructure"
        )
        self._my_frame.grid(
            row=0, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10)
        )
        self._my_frame.grid_columnconfigure(1, weight=1)
        self._my_frame.grid_rowconfigure(14, weight=1)

        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        self._frame_footer = ttk.Frame(master=root, height=30, style="Footer.TFrame")
        self._frame_footer.grid(
            row=1, column=0, sticky="swe", padx=10, pady=(5, 10), columnspan=0
        )
        self._frame_footer.grid_columnconfigure(1, weight=1)

    @property
    def my_frame(self) -> ttk.Labelframe:
        """Returns the my frame."""
        return self._my_frame

    @property
    def footer(self) -> ttk.Frame:
        """Returns the footer frame."""
        return self._frame_footer
