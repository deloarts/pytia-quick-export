from tkinter import StringVar
from typing import Literal

from const import KEEP
from helper.language import get_ui_language
from helper.lazy_loaders import LazyDocumentHelper
from pytia.exceptions import PytiaValueError
from resources import resource


def translate_source(value: int, language: Literal["en", "de"]) -> str:
    """
    Converts the CATIA source integer to the corresponding string.

    Args:
        value (int): The source integer.
        language (Literal[&quot;en&quot;, &quot;de&quot;]): The CATIA UI language.

    Raises:
        PytiaValueError: Raised if the language is not supported.

    Returns:
        str: The source string, dependent on the language.
    """
    if isinstance(value, int):
        match value:
            case 0:
                return (
                    resource.keywords.en.unknown
                    if language == "en"
                    else resource.keywords.de.unknown
                )
            case 1:
                return (
                    resource.keywords.en.made
                    if language == "en"
                    else resource.keywords.de.made
                )
            case 2:
                return (
                    resource.keywords.en.bought
                    if language == "en"
                    else resource.keywords.de.bought
                )
            case _:
                raise PytiaValueError(
                    f"Source value error: Cannot translate {value} to a CATIA source name."
                )


def translate_type(is_part: bool, language: Literal["en", "de"]) -> str:
    """
    Returns the type of the document dependent on the language.

    Args:
        is_part (bool): Wether to return the type for a part or a product.
        language (Literal[&quot;en&quot;, &quot;de&quot;]): The CATIA UI language.

    Raises:
        PytiaValueError: Raised if the language is not supported.

    Returns:
        str: The type string, dependent on the language.
    """
    if is_part:
        return (
            resource.keywords.en.part if language == "en" else resource.keywords.de.part
        )
    return (
        resource.keywords.en.assembly
        if language == "en"
        else resource.keywords.de.assembly
    )


def translate_project(project: StringVar, doc_helper: LazyDocumentHelper) -> str:
    return (
        doc_helper.document.properties.get_by_name(resource.props.project).value
        if project.get() == KEEP
        else project.get()
    )


def translate_property_value(
    value: str,
    selected_quantity: int | str,
    selected_condition: str,
    selected_project: str,
    doc_helper: LazyDocumentHelper,
) -> str:
    lang = get_ui_language(parameters=doc_helper.document.product.parameters)

    if value.startswith("$"):
        keyword_item = value.split("$")[-1]

        # Look for CATIA standard properties and handle them
        if keyword_item == "partnumber":
            value = doc_helper.document.product.part_number
        elif keyword_item == "revision":
            value = doc_helper.document.product.revision
        elif keyword_item == "definition":
            value = doc_helper.document.product.definition
        elif keyword_item == "source":
            value = translate_source(doc_helper.document.product.source, lang)
        elif keyword_item == "description":
            value = doc_helper.document.product.description_reference
        elif keyword_item == "type":
            value = translate_type(doc_helper.document.product.is_catpart(), lang)
        elif keyword_item == "quantity":
            value = str(selected_quantity)

    # Look for user properties and handle them.
    elif doc_helper.document.properties.exists(value):
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
                creator_logon := doc_helper.document.properties.get_by_name(value).value
            )
        ):
            value = resource.get_user_by_logon(creator_logon).name
        elif (
            value == resource.props.modifier
            and resource.settings.export.apply_username
            and resource.logon_exists(
                modifier_logon := doc_helper.document.properties.get_by_name(
                    value
                ).value
            )
        ):
            value = resource.get_user_by_logon(modifier_logon).name

        # Get the properties' value by the name
        else:
            value = doc_helper.document.properties.get_by_name(value).value
    else:
        value = ""

    return value
