"""
    Export submodule. Holds utility functions for handling data exports.
"""
from pathlib import Path
from typing import Literal

from pytia.wrapper.documents.part_documents import PyPartDocument
from pytia.wrapper.documents.product_documents import PyProductDocument


def _export_stp_stl(
    path: Path,
    filetype: Literal["stp", "stl"],
    document: PyProductDocument | PyPartDocument,
) -> None:
    """
    Exports the data into a file. The file will be exported into the temp folder and moved
    after the main task has finished.

    Args:
        path (Path): The full export path (folder, filename and extension).
        filetype (str): The type of the file to be exported (stp or stl).
        document (PyProductDocument | PyPartDocument): The document from which to export the data.
    """
    document.document.export_data(file_name=path, file_type=filetype, overwrite=True)


def export_stp(
    path: Path,
    document: PyProductDocument | PyPartDocument,
) -> None:
    """
    Exports the data into a stp file. The file will be exported into the temp folder and moved
    after the main task has finished.

    Args:
        path (Path): The full export path (folder, filename and extension).
        document (PyProductDocument | PyPartDocument): The document from which to export the stp.
    """
    _export_stp_stl(filetype="stp", path=path, document=document)


def export_stl(
    path: Path,
    document: PyPartDocument,
) -> None:
    """
    Exports the data into a stl file. The file will be exported into the temp folder and moved
    after the main task has finished.

    Args:
        path (Path): The full export path (folder, filename and extension).
        document (PyProductDocument | PyPartDocument): The document from which to export the stl.
    """
    _export_stp_stl(filetype="stl", path=path, document=document)
