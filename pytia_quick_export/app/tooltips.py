"""
    Tooltips submodule for the app.
"""

from app.layout import Layout
from app.vars import Variables
from const import KEEP
from helper.outlook import get_outlook
from pytia_ui_tools.handlers.workspace_handler import Workspace
from pytia_ui_tools.widgets.tooltips import ToolTip
from resources import resource


class ToolTips:
    """
    The ToolTips class. Responsible for initializing all tooltips for the main windows widgets.
    """

    def __init__(
        self, layout: Layout, workspace: Workspace, variables: Variables
    ) -> None:
        """
        Inits the ToolTips class.

        Args:
            layout (Layout): The layout of the main window.
            workspace (Workspace): The workspace instance.
            variables (Variables): The variables of the main window.
        """

        # region PROJECT NUMBER
        project_tooltip = (
            f"If set to {KEEP!r} the project number will be used from the part or product "
            "properties. Otherwise the project number will be overwritten with the value from "
            "this input field."
        )
        if (
            resource.settings.restrictions.strict_project
            and workspace.elements.projects
        ):
            project_tooltip += (
                "\n\nThe rule for project numbers is set to 'strict'.\n\n"
                "You can only use project numbers that are set in the workspace file."
            )
        elif (
            resource.settings.restrictions.strict_project
            and workspace.available
            and not workspace.elements.projects
        ):
            project_tooltip += (
                "\n\nThe rule for project numbers is set to 'strict'.\n\n"
                "Warning: There are no project numbers set in the workspace file, you are "
                "allowed to use any project number of your choice. But it is recommended to "
                "setup the workspace file correctly."
            )
        elif resource.settings.restrictions.strict_project and not workspace.available:
            project_tooltip += (
                "\n\nThe rule for project numbers is set to 'strict'.\n\n"
                "Warning: No workspace file found. You are allowed to use any project number "
                "but you should consider setting up the workspace file correctly."
            )
        ToolTip(widget=layout.input_project, text=project_tooltip)

        # endregion

        # region CONDITION
        ToolTip(
            widget=layout.input_condition,
            text=(
                "The condition for the export:\n\n"
                f"{resource.settings.condition.new.name!r}: The document will be exported with "
                "all properties, in the same way as it would've been exported with the "
                "PYTIA Bill of Material App.\n\n"
                f"{resource.settings.condition.mod.name!r}: The document will be exported without "
                f"the properties {' ,'.join(resource.settings.condition.mod.overwrite.keys())}."
            ),
        )
        # endregion

        # region QUANTITY
        ToolTip(widget=layout.input_quantity, text="Must be greater than zero.")
        # endregion

        # region NOT
        ToolTip(
            widget=layout.help_note,
            text=(
                "The note will only be visible in the e-mail body. If you want to leave a "
                "permanent note, please use the PYTIA Property Manager."
            ),
            delay_ms=1,
        )
        # endregion

        # region MAIL
        mail_tooltip = (
            "Select the email address to which you want to send the exported data."
        )
        if get_outlook() is None:
            mail_tooltip += "\n\nDisabled, because MS Outlook is not available."
        ToolTip(widget=layout.input_mail, text=mail_tooltip)
        # endregion

        # region UPLOAD
        if resource.settings.export.enable_rps:
            upload_tooltip = (
                f"Upload the data of the item directly to {resource.rps.name}.\n\n"
                "The following conditions have to be met, to enable a direct upload:\n"
                " - The source of the document must be 'bought'\n"
                " - A project number must be selected\n"
                f" - The condition must be {resource.settings.condition.new.name!r}\n"
                " - The quantity must be greater than zero\n"
                " - Your personal access token must be setup\n"
            )
            ToolTip(widget=layout.button_upload, text=upload_tooltip)
        # endregion
