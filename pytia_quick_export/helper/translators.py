from typing import Literal

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
