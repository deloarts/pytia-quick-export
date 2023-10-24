"""
    Helps collecting and handling the documents data.
"""

from dataclasses import asdict
from typing import List

from helper.language import get_ui_language
from helper.lazy_loaders import LazyDocumentHelper
from helper.translators import translate_property_value
from models.data import DataModel
from models.data import DatumModel
from pytia.log import log
from resources import resource


def collect_data(
    doc_helper: LazyDocumentHelper,
    selected_quantity: int | str,
    selected_condition: str,
    selected_project: str,
) -> DataModel:
    """
    Collects the data from the document, and further:

    - uses the header items depending on the document's source
    - takes the `header_items` from the excel.json config file and puts those items  and their \
        corresponding values into the DataModel object
    - translates all `header_items` according to the keywords.json config file
    - applies the `condition` settings from the settings.json config file
    - applies the `apply_username` setting from the settings.json config file
    - overwrites the `project` property with the `selected_project` property (only for the export, \
        the documents project-property won't be changed)

    Args:
        doc_helper (LazyDocumentHelper): The doc helper instance from which to \
            retrieve the data.
        selected_quantity (int | str): The quantity from the UI.
        selected_condition (str): The condition from the UI.
        selected_project (str): The project from the UI.

    Returns:
        DataModel: The data as DataModel object.
    """
    header_items = (
        resource.excel.header_items_made
        if doc_helper.source == 1
        else resource.excel.header_items_bought
    )
    data: List[DatumModel] = []

    for index, header_item in enumerate(header_items):
        log.info(f"Gathering data from item {header_item!r}...")
        value = ""
        name = None

        # Look for fixed text elements
        if "=" in header_item:
            name, value = get_fixed_text(header_item)

        # Look for property elements
        elif ":" in header_item:
            name, value = get_property(
                header_item=header_item,
                doc_helper=doc_helper,
                selected_quantity=selected_quantity,
                selected_condition=selected_condition,
                selected_project=selected_project,
            )

        # Look for placeholder columns
        else:
            name = header_item

        data.append(DatumModel(index=index, name=name, value=value))

    return DataModel(data)


def get_fixed_text(header_item: str) -> tuple:
    """
    Returns the name and value of a fixed text from the given header name.
    This is bound to the rules for the header_items_made and header_items_bought from
    the excel.json (see DEFAULT_FILES.md).

    Args:
        header_item (str): The header item from which to retrieve the property name \
            and data.

    Returns:
        tuple: The name (column name) and the fixed text for the item.
    """
    name, value = header_item.split("=")
    return name, value


def get_property(
    header_item: str,
    doc_helper: LazyDocumentHelper,
    selected_quantity: int | str,
    selected_condition: str,
    selected_project: str,
) -> tuple:
    """
    Returns the name and value of a property from the given header name.
    This is bound to the rules for the header_items_made and header_items_bought from
    the excel.json (see DEFAULT_FILES.md).

    Args:
        header_item (str): The header item from which to retrieve the property name \
            and data.
        doc_helper (LazyDocumentHelper): The doc helper instance from which to \
            retrieve the data.
        selected_quantity (int | str): The quantity from the UI.
        selected_condition (str): The condition from the UI.
        selected_project (str): The project from the UI.

    Returns:
        tuple: The name (column name) and the data from the property.
    """
    lang = get_ui_language(parameters=doc_helper.document.product.parameters)
    keywords = asdict(resource.keywords.en if lang == "en" else resource.keywords.de)

    name, value = header_item.split(":")

    # Translate name, if keyword
    if value.startswith("$") and (kw_key := value.split("$")[1]) in keywords:
        name = keywords[kw_key]

    # Translate the value
    value = translate_property_value(
        value=value,
        selected_quantity=selected_quantity,
        selected_condition=selected_condition,
        selected_project=selected_project,
        doc_helper=doc_helper,
    )

    return name, value
