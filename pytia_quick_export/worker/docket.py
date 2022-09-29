"""
    Export submodule. Holds utility functions for handling data exports.
"""
from pathlib import Path

from const import LOGON
from pytia.exceptions import PytiaFileOperationError
from pytia.utilities.docket import (
    DocketConfig,
    create_docket_from_template,
    export_docket_as_pdf,
)
from pytia.wrapper.documents.part_documents import PyPartDocument
from pytia.wrapper.documents.product_documents import PyProductDocument
from resources import resource
from templates import templates


def export_docket(
    path: Path,
    document: PyProductDocument | PyPartDocument,
    config: DocketConfig,
    condition: str,
    **kwargs,
) -> None:
    """
    Exports the docket into a PDF file. The docket will be exported into the temp folder and moved
    after the main task has finished.

    Args:
        path (Path): The full export path (folder, filename and extension).
        document (PyPartDocument | PyProductDocument): The part or product document from which \
            to create the docket
        config (DocketConfig): The docket configuration object.

        kwargs: Keyword arguments will be added to the docket for text elements which names are \
            prefixed with `arg.`. Example: To add the quantity to the docket text \
            element with the name 'arg.quantity' you have to supply the argument `quantity=1`.

    Raises:
        PytiaFileOperationError: Raised if the given folder isn't valid.
    """
    if templates.docket_path is None:
        raise PytiaFileOperationError(
            "Cannot export docket, template file doesn't exist."
        )

    # Translate creator username
    if document.properties.exists(resource.props.creator):
        if (
            resource.logon_exists(
                creator_logon := document.properties.get_by_name(
                    resource.props.creator
                ).value
            )
            and resource.settings.export.apply_username
        ):
            creator = resource.get_user_by_logon(creator_logon).name
        else:
            creator = creator_logon
    else:
        creator = "Unknown"

    # Translate modifier username
    if document.properties.exists(resource.props.modifier):
        if (
            resource.logon_exists(
                modifier_logon := document.properties.get_by_name(
                    resource.props.modifier
                ).value
            )
            and resource.settings.export.apply_username
        ):
            modifier = resource.get_user_by_logon(modifier_logon).name
        else:
            modifier = modifier_logon
    else:
        modifier = "Unknown"

    # Translate publisher username
    if resource.logon_exists(LOGON) and resource.settings.export.apply_username:
        publisher = resource.get_user_by_logon(LOGON).name
    else:
        publisher = LOGON

    # Apply properties, where their values are dependent on the condition.
    condition_props = {}
    if condition == resource.settings.condition.mod.name:
        condition_props = resource.settings.condition.mod.overwrite
    else:
        for prop in resource.settings.condition.mod.overwrite:
            if document.properties.exists(prop):
                condition_props[prop] = document.properties.get_by_name(prop).value
            else:
                condition_props[prop] = ""

    docket = create_docket_from_template(
        template=templates.docket_path,
        document=document,
        config=config,
        hide_unknown_properties=True,
        creator=creator,
        modifier=modifier,
        publisher=publisher,
        **condition_props,
        **kwargs,
    )
    export_docket_as_pdf(
        docket=docket,
        name=path.name,
        folder=path.resolve().parent,
    )
