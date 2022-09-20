"""
    Submodule for language related functions.
"""

from typing import Literal

from pytia.framework.knowledge_interfaces.parameters import Parameters
from pytia.framework.product_structure_interfaces.product import Product
from pytia.log import log
from resources import resource


def get_ui_language(parameters: Parameters) -> Literal["en", "de"]:
    """
    Returns the language of the CATIA UI.

    Returns:
        Literal["en", "de"]: The language of the CATIA UI.
    """
    try:
        parameters.get_item(resource.keywords.en.partnumber)
        log.debug("UI language is set to 'English'.")
        return "en"
    except:
        pass

    try:
        parameters.get_item(resource.keywords.de.partnumber)
        log.debug("UI language is set to 'German'.")
        return "de"
    except:
        pass

    raise Exception(
        f"The selected language is not supported. "
        "Please select either 'English' or 'German'."
    )
