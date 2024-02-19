"""
    Export submodule. Holds utility functions for handling data exports.
"""

from pathlib import Path
from tkinter import messagebox as tkmsg

from const import PROP_DRAWING_PATH
from pytia.log import log
from pytia.wrapper.documents.drawing_documents import PyDrawingDocument
from pytia.wrapper.documents.part_documents import PyPartDocument
from pytia.wrapper.documents.product_documents import PyProductDocument
from pytia_ui_tools.handlers.workspace_handler import Workspace
from resources import resource
from resources.utils import expand_env_vars


def export_drawing(
    pdf_path: Path,
    dxf_path: Path,
    document: PyProductDocument | PyPartDocument,
    workspace: Workspace,
) -> None:
    """
    Exports the drawing into a pdf and dxf file. The files will be exported into the temp folder
    and moved after the main task has finished.

    This export only works if the 'pytia.drawing_path' property is set and valid. This property
    is created when using the https://github.com/deloarts/pytia-title-block app.

    Args:
        path (Path): The full export path (folder, filename and extension).
        document (PyProductDocument | PyPartDocument): The document from which to export the data.
    """
    if document.properties.exists(PROP_DRAWING_PATH):
        drawing_file_value = document.properties.get_by_name(PROP_DRAWING_PATH).value

        # When the linked drawing path starts with a dot, the path is assumed to be
        # relative to the workspace file.
        # This makes it possible to move a whole project without breaking the paths.
        if drawing_file_value.startswith(".\\") and workspace.workspace_folder:
            relative_path = Path(drawing_file_value[2:])
            drawing_path = Path(workspace.workspace_folder, relative_path)

        # If the linked drawing path isn't saved relative to a workspace file, it's
        # assumed to be either a full absolute path, or a symlinked path (e.g. onedrive)
        else:
            drawing_path = Path(expand_env_vars(drawing_file_value))

        if drawing_path.exists():
            with PyDrawingDocument() as drawing_document:
                drawing_document.open(drawing_path)
                drawing_document.drawing_document.export_data(
                    pdf_path, "pdf", overwrite=True
                )
                drawing_document.drawing_document.export_data(
                    dxf_path, "dxf", overwrite=True
                )
                if resource.settings.export.lock_drawing_views:
                    sheets = drawing_document.drawing_document.sheets
                    for i_sheet in range(1, sheets.count + 1):
                        sheet = sheets.item(i_sheet)
                        for i_view in range(3, sheet.views.count + 1):
                            view = sheet.views.item(i_view)
                            view.lock_status = True
                            log.info(
                                f"Locked view {view.name!r} or sheet {sheet.name!r}."
                            )
                    drawing_document.save()
        else:
            msg = (
                f"Skipped drawing export of {document.document.name!r}: Path not valid."
            )
            log.error(msg)
            tkmsg.showerror(title=resource.settings.title, message=msg)
    else:
        log.info(f"Skipped drawing export of {document.document.name!r}: Path not set.")
