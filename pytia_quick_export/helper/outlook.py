from typing import Optional

from pytia.log import log
from win32com.client import CDispatch
from win32com.client import Dispatch
from win32com.server.exception import COMException


def get_outlook() -> Optional[CDispatch]:
    """
    Connects to the outlook application dispatcher. Returns None if Outlook is not installed \
        on this system.

    Returns:
        Optional[CDispatch]: The dispatch from MS Outlook.
    """
    try:
        app = Dispatch("outlook.application")
        return app  # type: ignore
    except COMException as e:
        log.warning(f"Outlook is not installed on this system: {e}")
        return None
    except Exception as e:  # pylint: disable=broad-except
        log.error(f"Failed connecting to MS Outlook: {e}")
        return None
