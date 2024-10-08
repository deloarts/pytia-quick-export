"""
    The main task of the app: Exporting stuff.
"""

import os
from datetime import datetime
from pathlib import Path
from tkinter import Tk
from tkinter import messagebox as tkmsg

import validators
from app.frames import Frames
from app.layout import Layout
from app.state_setter import UISetter
from app.vars import Variables
from const import KEEP
from const import TEMP_ATTACHMENTS
from const import TEMP_EXPORT
from helper.lazy_loaders import LazyDocumentHelper
from helper.names import get_data_export_name
from helper.translators import translate_project
from models.data import DataModel
from pytia.log import log
from pytia.utilities.docket import DocketConfig
from pytia.wrapper.documents.part_documents import PyPartDocument
from pytia_ui_tools.handlers.workspace_handler import Workspace
from pytia_ui_tools.utils.files import file_utility
from pytia_ui_tools.utils.qr import QR
from resources import resource

from .data import collect_data
from .docket import export_docket
from .drawing import export_drawing
from .excel import export_excel
from .mail import export_mail
from .runner import Runner
from .stp_stl import export_stl
from .stp_stl import export_stp


class Worker:
    """The worker class. Responsible for running all sub-tasks to export data."""

    def __init__(
        self,
        main_ui: Tk,
        layout: Layout,
        ui_setter: UISetter,
        doc_helper: LazyDocumentHelper,
        variables: Variables,
        frames: Frames,
        workspace: Workspace,
    ) -> None:
        self.main_ui = main_ui
        self.layout = layout
        self.ui_setter = ui_setter
        self.doc_helper = doc_helper
        self.variables = variables
        self.frames = frames
        self.workspace = workspace

        self.data: DataModel

        self.project = translate_project(
            project=self.variables.project, doc_helper=self.doc_helper
        )
        self.product = self.doc_helper.document.properties.get_by_name(
            resource.props.product
        ).value
        self.partnumber = self.doc_helper.document.product.part_number
        self.revision = self.doc_helper.document.product.revision

        self.export_folder = Path(
            TEMP_EXPORT, datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        )
        self.attachments_folder = Path(
            TEMP_ATTACHMENTS, datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        )

        self.export_name = get_data_export_name(self.doc_helper)
        self.export_name_with_project = get_data_export_name(
            self.doc_helper, project=self.project
        )

        self.docket_path = Path(
            self.export_folder, self.export_name_with_project + ".pdf"
        )
        self.xlsx_path = Path(
            self.export_folder, self.export_name_with_project + ".xlsx"
        )
        self.stp_path = Path(self.export_folder, self.export_name + ".stp")
        self.stl_path = Path(self.export_folder, self.export_name + ".stl")
        self.dxf_path = Path(self.export_folder, self.export_name + ".dxf")
        self.pdf_path = Path(self.export_folder, self.export_name + ".pdf")

        self.runner = Runner(
            root=self.main_ui,
            callback_variable=self.variables.progress,
        )
        self.runner.add(self._collect_data, name="Collect data")
        self.runner.add(self._export_excel, name="EXCEL export")
        if self.doc_helper.document.product.source == 1:  # Source: Made
            self.runner.add(self._export_stp_stl, name="STEP/STL export")
            self.runner.add(self._export_docket, name="Docket export")
            self.runner.add(self._export_drawing, name="Drawing export")

        self.runner.add(self._send_mail, name="Sending mail")
        self.runner.add(self._clean, name="Cleaning up")

    def run(self) -> None:
        """Runs all tasks."""
        os.makedirs(self.export_folder)
        self.runner.run_tasks()

        tkmsg.showinfo(
            title=resource.settings.title, message="Export completed successfully."
        )

        if resource.settings.export.close_app_after:
            self.main_ui.after(200, self.main_ui.destroy)
        else:
            self.ui_setter.normal()

    def _collect_data(self) -> None:
        """Retrieves the data from the document."""
        self.data = collect_data(
            doc_helper=self.doc_helper,
            selected_quantity=self.variables.quantity.get(),
            selected_condition=self.variables.condition.get(),
            selected_project=self.project,
        )

    def _export_excel(self) -> None:
        """Exports the EXCEL file, containing all information about the document."""
        # Source: 0=Unknown, 1=Made, 2=Bought
        source = self.doc_helper.document.product.source

        export_excel(
            path=self.xlsx_path,
            selected_project=self.project,
            data=self.data,
            source="made" if source == 1 else "bought",
        )

    def _export_stp_stl(self) -> None:
        """Exports the 3D data as STL and STEP (STL only for parts)."""
        if isinstance(self.doc_helper.document, PyPartDocument):
            export_stl(path=self.stl_path, document=self.doc_helper.document)
        export_stp(path=self.stp_path, document=self.doc_helper.document)

    def _export_docket(self) -> None:
        """Generates a docket file as pdf."""
        qr = QR()
        qr.generate(
            data={
                "project": self.project,
                "product": self.product,
                "partnumber": self.partnumber,
                "revision": self.revision,
            }
        )
        qr_path = qr.save(
            path=Path(
                TEMP_EXPORT,
                file_utility.get_random_filename(filetype="png"),
            )
        )
        file_utility.add_delete(path=qr_path, skip_silent=True)

        export_docket(
            path=self.docket_path,
            document=self.doc_helper.document,
            config=DocketConfig.from_dict(resource.docket),
            selected_condition=self.variables.condition.get(),
            project=self.project,
            quantity=self.variables.quantity.get(),
            qr_path=qr_path,
        )

    def _export_drawing(self) -> None:
        """Exports the 2D data of the linked drawing (if there is one)."""
        export_drawing(
            pdf_path=self.pdf_path,
            dxf_path=self.dxf_path,
            document=self.doc_helper.document,
            workspace=self.workspace,
        )

    def _send_mail(self) -> None:
        """Sends the mail."""
        if validators.email(self.variables.mail.get()):  # type: ignore
            export_mail(
                data=self.data,
                selected_project=self.project,
                selected_condition=self.variables.condition.get(),
                selected_receiver=self.variables.mail.get(),
                note=self.variables.note.get(),
                attachments_folder=self.attachments_folder,
                data_folder=self.export_folder,
            )

    def _clean(self) -> None:
        """Deletes and moves files."""
        if os.path.exists(self.attachments_folder):
            for file in os.listdir(self.attachments_folder):
                file_utility.add_delete(path=Path(self.attachments_folder, file))

        export_files = os.listdir(self.export_folder)
        target_folder = Path(self.variables.folder.get())

        if target_folder.is_absolute() and target_folder.is_dir():
            for file in export_files:
                file_utility.add_move(
                    source=Path(self.export_folder, file),
                    target=Path(target_folder, file),
                )
        else:
            for file in export_files:
                file_utility.add_delete(path=Path(self.export_folder, file))

        file_utility.move_all()
