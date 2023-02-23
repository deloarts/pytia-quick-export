"""
    Helps collecting and handling the documents data.
"""

from dataclasses import asdict
from typing import List, Literal

from helper.language import get_ui_language
from helper.translators import translate_source, translate_type
from models.data import DataModel, DatumModel
from pytia.log import log
from pytia.wrapper.documents.part_documents import PyPartDocument
from pytia.wrapper.documents.product_documents import PyProductDocument
from resources import resource


def collect_data(
    document: PyProductDocument | PyPartDocument,
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
        document (PyProductDocument | PyPartDocument): The doc from which to retrieve the data.
        selected_quantity (int | str): The quantity from the UI.
        selected_condition (str): The condition from the UI.
        selected_project (str): The project from the UI.

    Returns:
        DataModel: The data as DataModel object.
    """
    header_items = (
        resource.excel.header_items_made
        if document.product.source == 1
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
                document=document,
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
    document: PyProductDocument | PyPartDocument,
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
        document (PyProductDocument | PyPartDocument): The doc from which to retrieve \
            the data.
        selected_quantity (int | str): The quantity from the UI.
        selected_condition (str): The condition from the UI.
        selected_project (str): The project from the UI.

    Returns:
        tuple: The name (column name) and the data from the property.
    """
    lang = get_ui_language(parameters=document.product.parameters)
    keywords = asdict(resource.keywords.en if lang == "en" else resource.keywords.de)

    name, value = header_item.split(":")
    if value.startswith("$"):
        keyword_item = value.split("$")[-1]

        # Translate the keyword item
        if (kw_key := value.split("$")[1]) in keywords:
            name = keywords[kw_key]

        # Look for CATIA standard properties and handle them
        if keyword_item == "partnumber":
            value = document.product.part_number
        elif keyword_item == "revision":
            value = document.product.revision
        elif keyword_item == "definition":
            value = document.product.definition
        elif keyword_item == "source":
            value = translate_source(document.product.source, lang)
        elif keyword_item == "description":
            value = document.product.description_reference
        elif keyword_item == "type":
            value = translate_type(document.product.is_catpart(), lang)
        elif keyword_item == "quantity":
            value = str(selected_quantity)

    # Look for user properties and handle them.
    elif document.properties.exists(value):
        # Apply rule for overwriting data depending on the selected condition
        if (
            selected_condition == resource.settings.condition.mod.name
            and value in resource.settings.condition.mod.overwrite
        ):
            value = resource.settings.condition.mod.overwrite[value]

        # Apply the project number
        elif value == resource.props.project:
            value = selected_project

        # Apply (translate) the username
        elif (
            value == resource.props.creator
            and resource.settings.export.apply_username
            and resource.logon_exists(
                creator_logon := document.properties.get_by_name(value).value
            )
        ):
            value = resource.get_user_by_logon(creator_logon).name
        elif (
            value == resource.props.modifier
            and resource.settings.export.apply_username
            and resource.logon_exists(
                modifier_logon := document.properties.get_by_name(value).value
            )
        ):
            value = resource.get_user_by_logon(modifier_logon).name

        # Get the properties' value by the name
        else:
            value = document.properties.get_by_name(value).value
    else:
        value = ""

    return name, value
