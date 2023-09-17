"""
    The callbacks submodule for the main window.
"""

from pathlib import Path, WindowsPath
from tkinter import Tk, filedialog

from app.frames import Frames
from app.layout import Layout
from app.state_setter import UISetter
from app.vars import Variables
from helper.lazy_loaders import LazyDocumentHelper
from helper.rps import Rps
from pytia.log import log
from pytia_ui_tools.handlers.workspace_handler import Workspace
from pytia_ui_tools.helper.values import add_current_value_to_combobox_list
from resources import resource
from worker import Worker


class Callbacks:
    """The callbacks class for the main window."""

    def __init__(
        self,
        root: Tk,
        variables: Variables,
        layout: Layout,
        frames: Frames,
        ui_setter: UISetter,
        workspace: Workspace,
        doc_helper: LazyDocumentHelper,
    ) -> None:
        """
        Initializes the callbacks class.

        Args:
            root (Tk): The main window of the app.
            variables (Variables): The variables of the main window.
            layout (Layout): The layout of the main window.
            ui_setter (UISetter): The ui setter instance of the main window.
        """
        self.root = root
        self.vars = variables
        self.layout = layout
        self.frames = frames
        self.workspace = workspace
        self.doc_helper = doc_helper
        self.set_ui = ui_setter
        self.readonly = bool(
            not resource.logon_exists()
            and not resource.settings.restrictions.allow_all_users
        )

        self._bind_menu_callbacks()
        self._bind_button_callbacks()
        self._bind_widget_callbacks()
        log.info("Callbacks initialized.")

    def _bind_menu_callbacks(self) -> None:
        """Binds all callbacks to the menubar."""
        if self.layout.rps_menu:
            self.layout.rps_menu.entryconfig(
                0, command=lambda: Rps.setup_personal_access_token(self.root)
            )
            self.layout.rps_menu.entryconfig(
                1, command=Rps.remove_personal_access_token
            )
            self.layout.rps_menu.entryconfig(2, command=Rps.test_login)

    def _bind_button_callbacks(self) -> None:
        """Binds all callbacks to the main windows buttons."""
        self.layout.button_increase_qty.configure(command=self.on_btn_increase_qty)
        self.layout.button_decrease_qty.configure(command=self.on_btn_decrease_qty)
        self.layout.button_browse_folder.configure(command=self.on_btn_export_folder)
        self.layout.button_export.configure(command=self.on_btn_export)
        self.layout.button_upload.configure(command=self.on_btn_upload)
        self.layout.button_abort.configure(command=self.on_btn_abort)

    def _bind_widget_callbacks(self) -> None:
        """Binds all callbacks to the main windows widgets."""
        if not (
            resource.settings.restrictions.strict_project
            and self.workspace.elements.projects
        ):
            self.layout.input_project.bind(
                "<FocusOut>",
                lambda _: add_current_value_to_combobox_list(self.layout.input_project),
            )

    def on_btn_increase_qty(self) -> None:
        """Callback function for the increase quantity button."""
        try:
            self.vars.quantity.set(str(int(self.vars.quantity.get()) + 1))
        except ValueError:
            self.vars.quantity.set("1")

    def on_btn_decrease_qty(self) -> None:
        """Callback function for the decrease quantity button."""
        try:
            value = int(self.vars.quantity.get())
            self.vars.quantity.set(str(value - 1) if value > 1 else "1")
        except ValueError:
            self.vars.quantity.set("1")

    def on_btn_export(self) -> None:
        """
        Event handler for the Export button. Verifies the user input and saves the changes to the
        documents properties.
        """
        log.info("Callback for button 'Export'.")
        self.set_ui.working()
        worker = Worker(
            main_ui=self.root,
            layout=self.layout,
            ui_setter=self.set_ui,
            doc_helper=self.doc_helper,
            variables=self.vars,
            frames=self.frames,
        )
        self.root.after(100, worker.run)

    def on_btn_upload(self) -> None:
        """
        Event handler for the Upload button. Verifies the user input and saves the changes to the
        documents properties.
        """
        log.info("Callback for button 'Upload'.")
        self.set_ui.working()
        rps = Rps(
            main_ui=self.root,
            ui_setter=self.set_ui,
            doc_helper=self.doc_helper,
            variables=self.vars,
        )
        self.root.after(100, rps.upload_bought_item)

    def on_btn_abort(self) -> None:
        """Callback function for the abort button. Closes the app."""
        log.info("Callback for button 'Abort'.")
        self.root.withdraw()
        self.root.destroy()

    def on_btn_export_folder(self) -> None:
        """
        Event handler for the browse export folder button. Asks the user to select a folder,
        into which to export the files.
        """
        log.info("Callback for button 'Browse docket folder'.")

        initial_dir = Path(self.vars.folder.get())
        if (
            not initial_dir.is_absolute()
            and self.workspace.workspace_folder
            and self.workspace.workspace_folder.exists()
        ):
            initial_dir = self.workspace.workspace_folder

        if path := WindowsPath(
            filedialog.askdirectory(
                initialdir=initial_dir,
                title=resource.settings.title,
            )
        ):
            self.vars.folder.set(str(path))
