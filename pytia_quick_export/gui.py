"""
    The main window for the application.
"""

import tkinter as tk
from pathlib import Path
from tkinter import font

import ttkbootstrap as ttk
from app.callbacks import Callbacks
from app.controller import Controller
from app.frames import Frames
from app.layout import Layout
from app.state_setter import UISetter
from app.tooltips import ToolTips
from app.traces import Traces
from app.vars import Variables
from const import APP_VERSION
from const import LOG
from const import LOGS
from helper.lazy_loaders import LazyDocumentHelper
from helper.messages import show_help
from helper.rps import Rps
from pytia.exceptions import PytiaBodyEmptyError
from pytia.exceptions import PytiaDifferentDocumentError
from pytia.exceptions import PytiaDocumentNotSavedError
from pytia.exceptions import PytiaNoDocumentOpenError
from pytia.exceptions import PytiaPropertyNotFoundError
from pytia.exceptions import PytiaWrongDocumentTypeError
from pytia_ui_tools.exceptions import PytiaUiToolsOutsideWorkspaceError
from pytia_ui_tools.handlers.error_handler import ErrorHandler
from pytia_ui_tools.handlers.mail_handler import MailHandler
from pytia_ui_tools.handlers.workspace_handler import Workspace
from pytia_ui_tools.window_manager import WindowManager
from resources import resource


class GUI(tk.Tk):
    """The user interface of the app."""

    WIDTH = 350
    HEIGHT = 450

    def __init__(self) -> None:
        """Inits the main window."""
        ttk.tk.Tk.__init__(self)
        self.style = ttk.Style(theme=resource.appdata.theme)

        # CLASS VARS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.doc_helper: LazyDocumentHelper  # Instantiate later for performance improvement
        self.workspace: Workspace  # Instantiate later, dependent on doc_helper
        self.set_ui: UISetter  # Instantiate later, dependent on doc_helper
        self.vars = Variables(root=self)
        self.frames = Frames(root=self)
        self.layout = Layout(
            root=self,
            frames=self.frames,
            variables=self.vars,
        )

        self.readonly = bool(
            not resource.logon_exists()
            and not resource.settings.restrictions.allow_all_users
        )

        # UI TOOLS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.window_manager = WindowManager(self)
        self.mail_handler = MailHandler(
            standard_receiver=resource.settings.mails.admin,
            app_title=resource.settings.title,
            app_version=APP_VERSION,
            logfile=Path(LOGS, LOG),
        )
        self.error_handler = ErrorHandler(
            mail_handler=self.mail_handler,
            warning_exceptions=[
                PytiaNoDocumentOpenError,
                PytiaWrongDocumentTypeError,
                PytiaBodyEmptyError,
                PytiaPropertyNotFoundError,
                PytiaDifferentDocumentError,
                PytiaDocumentNotSavedError,
                PytiaUiToolsOutsideWorkspaceError,
            ],
        )

        # UI INIT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.title(
            f"{resource.settings.title} "
            f"{'(DEBUG MODE)' if resource.settings.debug else APP_VERSION}"
            f"{' (READ ONLY)' if self.readonly else ''}"
        )
        self.attributes("-topmost", True)
        self.attributes("-toolwindow", True)
        self.config(cursor="wait")
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Segoe UI", size=9)
        self.report_callback_exception = self.error_handler.exceptions_callback

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (GUI.WIDTH / 2))
        y_coordinate = int((screen_height / 2) - (GUI.HEIGHT / 2) - 20)
        self.geometry(f"{GUI.WIDTH}x{GUI.HEIGHT}+{x_coordinate}+{y_coordinate}")
        self.minsize(width=GUI.WIDTH, height=GUI.HEIGHT)

        self.update()
        self.window_manager.remove_window_buttons()

    def run(self) -> None:
        """Run the app."""
        self.after(100, self._run)
        self.mainloop()

    def _run(self) -> None:
        """Runs all controllers. Initializes all lazy loaders, bindings and traces."""
        self.doc_helper = LazyDocumentHelper()
        self.workspace = Workspace(
            path=self.doc_helper.path,
            filename=resource.settings.files.workspace,
            allow_outside_workspace=resource.settings.restrictions.allow_outside_workspace,
        )
        self.workspace.read_yaml()
        if ws_title := self.workspace.elements.title:
            self.title(f"{self.title()}  -  {ws_title} (Workspace)")

        self.set_ui = UISetter(
            root=self,
            layout=self.layout,
            variables=self.vars,
            workspace=self.workspace,
            source=self.doc_helper.source,
        )

        controller = Controller(
            root=self,
            doc_helper=self.doc_helper,
            layout=self.layout,
            vars=self.vars,
            ui_setter=self.set_ui,
            workspace=self.workspace,
        )
        controller.run_all_controllers()

        self.callbacks()
        self.traces()
        self.bindings()
        self.tooltips()

    def bindings(self) -> None:
        """Key bindings."""
        self.bind("<Escape>", lambda _: self.destroy())
        self.bind("<F1>", lambda _: show_help())
        self.bind("<F6>", lambda _: Rps.setup_personal_access_token(self))
        # FIXME: There is a bug on the middle mouse button, where, when the button is clicked,
        # selected text will be inserted into a widget, when the cursor hovers above the widget.
        # I can't find the source of the bug, this is a to do.
        # self.bind("<Button-2>", lambda _: self.on_btn_save())

    def callbacks(self) -> None:
        """Instantiates the Callbacks class."""
        Callbacks(
            root=self,
            variables=self.vars,
            layout=self.layout,
            frames=self.frames,
            doc_helper=self.doc_helper,
            ui_setter=self.set_ui,
            workspace=self.workspace,
        )

    def traces(self) -> None:
        """Instantiates the traces class."""
        Traces(
            variables=self.vars,
            state_setter=self.set_ui,
            layout=self.layout,
            style=self.style,
            source=self.doc_helper.source,
        )

    def tooltips(self) -> None:
        """Instantiates the tooltips class."""
        ToolTips(layout=self.layout, workspace=self.workspace, variables=self.vars)
