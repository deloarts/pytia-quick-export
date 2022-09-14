"""
    Traces submodule for the app.
"""

from pytia.log import log

from app.state_setter import UISetter
from app.vars import Variables


class Traces:
    """The Traces class. Responsible for all variable traces in the main window."""

    def __init__(self, variables: Variables, state_setter: UISetter) -> None:
        """
        Inits the Traces class. Adds the main windows' variable traces.

        Args:
            vars (Variables): The main window's variables.
            state_setter (UISetter): The state setter of the main window.
        """
        self.vars = variables
        self.set_ui = state_setter

        self._add_traces()
        log.info("Traces initialized.")

    def _add_traces(self) -> None:
        """Adds all traces."""
        ...
