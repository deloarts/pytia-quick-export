"""
    Tooltips submodule for the app.
"""

from pytia_ui_tools.handlers.workspace_handler import Workspace
from pytia_ui_tools.widgets.tooltips import ToolTip
from resources import resource

from app.layout import Layout
from app.vars import Variables


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
        
        ToolTip()
