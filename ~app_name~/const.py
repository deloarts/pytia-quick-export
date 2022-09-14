"""
    Constants for the app.
"""

import os

__version__ = "0.1.0"

PYTIA = "pytia"
~APP_NAME~ = "~app_name~"
PYTIA_BOUNDING_BOX = "pytia_bounding_box"

APP_NAME = "~app-name~"
APP_VERSION = __version__

LOGON = str(os.environ.get("USERNAME"))
CNEXT = "win_b64\\code\\bin\\CNEXT.exe"
TEMP = str(os.environ.get("TEMP"))
APPDATA = f"{str(os.environ.get('APPDATA'))}\\{PYTIA}\\{~APP_NAME~}"
LOGS = f"{APPDATA}\\logs"
LOG = "app.log"
PID = os.getpid()
PID_FILE = f"{TEMP}\\{~APP_NAME~}.pid"
VENV = f"\\.env\\{APP_VERSION}"
VENV_PYTHON = VENV + "\\Scripts\\python.exe"
VENV_PYTHONW = VENV + "\\Scripts\\pythonw.exe"
PY_VERSION = APPDATA + "\\pyversion.txt"

CONFIG_APPDATA = "config.json"
CONFIG_SETTINGS = "settings.json"
CONFIG_DEPS = "dependencies.json"
CONFIG_DEPS_DEFAULT = "dependencies.default.json"
CONFIG_INFOS = "information.json"
CONFIG_INFOS_DEFAULT = "information.default.json"
CONFIG_USERS = "users.json"

WEB_PIP = "www.pypi.org"
