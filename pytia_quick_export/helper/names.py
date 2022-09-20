"""
    Helper for names.
"""

from const import KEEP
from pytia_ui_tools.handlers.workspace_handler import Workspace
from resources import resource

from helper.lazy_loaders import LazyDocumentHelper


def get_data_export_name(
    doc_helper: LazyDocumentHelper, project: str | None = None
) -> str:
    """
    Returns the filename for the data export.

    Args:
        doc_helper (LazyDocumentHelper): The lazy document helper instance.
        project (str | None, optional): The project number, that will be used. Defaults to None. \
            If None, the project number from the documents properties will be used.

    Returns:
        str: The filename.
    """
    # TODO: Make the export filename configurable in the settings.json

    value = (
        f"{doc_helper.document.properties.get_by_name(resource.props.machine).value} "
        f"{doc_helper.document.product.part_number} "
        f"Rev{doc_helper.document.product.revision}"
    )
    if project:
        value = f"{project} {value}"
    return value
