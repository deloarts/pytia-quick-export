"""
    Export submodule. Holds utility functions for handling data exports.
"""
from dataclasses import asdict
from pathlib import Path
from typing import Literal

from helper.language import get_ui_language
from helper.translators import translate_source, translate_type
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from pytia.log import log
from pytia.wrapper.documents.part_documents import PyPartDocument
from pytia.wrapper.documents.product_documents import PyProductDocument
from resources import resource


def export_excel(
    path: Path,
    document: PyProductDocument | PyPartDocument,
    project: str,
    quantity: int | str,
    condition: str,
) -> None:
    """
    Exports the EXCEL file containing all the information of the document.
    The EXCEL file will have two rows, the header and the data row.
    For configuration see the 'excel.json' resource file.

    Args:
        path (Path): The path into which to save the EXCEL (xlsx) file.
        document (PyProductDocument | PyPartDocument): The document from which to draw the data.
        project (str): The project number (from the UI).
        quantity (int | str): The quantity of the document (from the UI).
        condition (str): The condition (from the UI).
    """
    lang = get_ui_language(parameters=document.product.parameters)
    wb = Workbook()
    ws = wb.active
    ws.title = path.stem

    _write_data(
        worksheet=ws,
        document=document,
        project=project,
        quantity=quantity,
        condition=condition,
        language=lang,
    )
    _create_header(worksheet=ws, language=lang)
    _style_worksheet(worksheet=ws)

    wb.save(str(path))
    log.info(f"Saved excel document to {str(path)!r}.")


def _write_data(
    worksheet: Worksheet,
    document: PyProductDocument | PyPartDocument,
    project: str,
    quantity: int | str,
    condition: str,
    language: Literal["en", "de"],
) -> None:
    """
    Saves the documents data to the EXCEL doc.

    Args:
        worksheet (Worksheet): The EXCEL worksheet.
        document (PyProductDocument | PyPartDocument): The document from which to draw the data.
        project (str): The project number (from the UI).
        quantity (int | str): The quantity (from the UI).
        condition (str): The condition (from the UI).
        language (Literal[&quot;en&quot;, &quot;de&quot;]): The CATIA UI language.
    """
    for index, item in enumerate(resource.excel.header_items):
        cell_value: str = ""
        if item.startswith("$"):
            keyword_item = item.split("$")[-1]
            if keyword_item == "partnumber":
                cell_value = document.product.part_number
            elif keyword_item == "revision":
                cell_value = document.product.revision
            elif keyword_item == "definition":
                cell_value = document.product.definition
            elif keyword_item == "source":
                cell_value = translate_source(document.product.source, language)
            elif keyword_item == "description":
                cell_value = document.product.description_reference
            elif keyword_item == "type":
                cell_value = translate_type(document.product.is_catpart(), language)
            elif keyword_item == "quantity":
                cell_value = str(quantity)
        elif document.properties.exists(item):
            if (
                condition == resource.settings.condition.mod.name
                and item in resource.settings.condition.mod.overwrite
            ):
                cell_value = resource.settings.condition.mod.overwrite[item]
            elif item == resource.props.project:
                cell_value = project
            elif (
                item == resource.props.creator
                and resource.settings.export.apply_username_in_excel
                and resource.logon_exists(
                    creator_logon := document.properties.get_by_name(item).value
                )
            ):
                cell_value = resource.get_user_by_logon(creator_logon).name
            elif (
                item == resource.props.modifier
                and resource.settings.export.apply_username_in_excel
                and resource.logon_exists(
                    modifier_logon := document.properties.get_by_name(item).value
                )
            ):
                cell_value = resource.get_user_by_logon(modifier_logon).name
            else:
                cell_value = document.properties.get_by_name(item).value
        worksheet.cell(
            resource.excel.data_row + 1, index + 1
        ).value = cell_value  # type:ignore


def _create_header(worksheet: Worksheet, language: Literal["en", "de"]) -> None:
    """
    Creates a header row in the given worksheet.

    Args:
        worksheet (Worksheet): The worksheet into which to create the header row.
        language (Literal[&quot;en&quot;, &quot;de&quot;]): The CATIA UI language.
    """
    keywords = asdict(
        resource.keywords.en if language == "en" else resource.keywords.de
    )
    if isinstance(resource.excel.header_row, int):
        for index, item in enumerate(resource.excel.header_items):
            if item.startswith("$") and (key := item.split("$")[1]) in keywords:
                worksheet.cell(
                    resource.excel.header_row + 1, index + 1
                ).value = keywords[key]
            else:
                worksheet.cell(
                    resource.excel.header_row + 1, index + 1
                ).value = item  # type:ignore
        log.debug(f"Created header for worksheet {worksheet.title!r}")


def _style_worksheet(worksheet: Worksheet) -> None:
    """Styles the worksheet as stated in the excel.json config file."""
    for column_cells in worksheet.columns:
        # Set format, font and size
        for index, cell in enumerate(column_cells):
            if index > resource.excel.data_row - 1:
                color = (
                    resource.excel.data_color_1
                    if index % 2 == 0
                    else resource.excel.data_color_2
                )
                bg_color = (
                    resource.excel.data_bg_color_1
                    if index % 2 == 0
                    else resource.excel.data_bg_color_2
                )
                cell.fill = PatternFill(
                    start_color=bg_color, end_color=bg_color, fill_type="solid"
                )
            else:
                color = None
            cell.number_format = "@"
            cell.font = Font(
                name=resource.excel.font, size=resource.excel.size, color=color
            )
            cell.alignment = Alignment(horizontal="left", vertical="center")

        # Set font and height for the header row
        if isinstance(resource.excel.header_row, int):
            worksheet.row_dimensions[resource.excel.header_row + 1].height = 20
            column_cells[resource.excel.header_row].font = Font(
                name=resource.excel.font,
                size=resource.excel.size,
                bold=True,
                color=resource.excel.header_color,
            )
            column_cells[resource.excel.header_row].fill = PatternFill(
                start_color=resource.excel.header_bg_color,
                end_color=resource.excel.header_bg_color,
                fill_type="solid",
            )
            column_cells[resource.excel.header_row].alignment = Alignment(
                horizontal="center", vertical="center"
            )

        # Set cell width
        length = max(len(str(cell.value)) * 1.1 for cell in column_cells)
        worksheet.column_dimensions[column_cells[0].column_letter].width = (
            length if length > 2 else 2
        )

    log.info(f"Styled worksheet {worksheet.title!r}.")
