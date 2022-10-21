"""
    Helps collecting and handling the documents data.
"""

from dataclasses import asdict
from typing import List

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
    lang = get_ui_language(parameters=document.product.parameters)
    keywords = asdict(resource.keywords.en if lang == "en" else resource.keywords.de)
    items = (
        resource.excel.header_items_made
        if document.product.source == 1
        else resource.excel.header_items_bought
    )
    data: List[DatumModel] = []

    for index, item in enumerate(items):
        value = None
        name = item

        if item.startswith("$"):
            keyword_item = item.split("$")[-1]

            # Translate the keyword item
            if (kw_key := item.split("$")[1]) in keywords:
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

        # Look for user properties and handle them
        elif document.properties.exists(item):
            if (
                selected_condition == resource.settings.condition.mod.name
                and item in resource.settings.condition.mod.overwrite
            ):
                value = resource.settings.condition.mod.overwrite[item]
            elif item == resource.props.project:
                value = selected_project
            elif (
                item == resource.props.creator
                and resource.settings.export.apply_username
                and resource.logon_exists(
                    creator_logon := document.properties.get_by_name(item).value
                )
            ):
                value = resource.get_user_by_logon(creator_logon).name
            elif (
                item == resource.props.modifier
                and resource.settings.export.apply_username
                and resource.logon_exists(
                    modifier_logon := document.properties.get_by_name(item).value
                )
            ):
                value = resource.get_user_by_logon(modifier_logon).name
            else:
                value = document.properties.get_by_name(item).value

        data.append(DatumModel(index=index, name=name, value=value))

    return DataModel(data)
