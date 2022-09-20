"""
    Constants for the app.
"""

import os
from pathlib import Path

__version__ = "0.1.0"

PYTIA = "pytia"
PYTIA_QUICK_EXPORT = "pytia_quick_export"

APP_NAME = "PYTIA Quick Export"
APP_VERSION = __version__

LOGON = str(os.environ.get("USERNAME"))
CNEXT = "win_b64\\code\\bin\\CNEXT.exe"
TEMP = str(os.environ.get("TEMP"))
TEMP_EXPORT = Path(TEMP, PYTIA_QUICK_EXPORT, "export")
TEMP_ATTACHMENTS = Path(TEMP, PYTIA_QUICK_EXPORT, "attachments")
TEMP_TEMPLATES = Path(TEMP, PYTIA_QUICK_EXPORT, "templates")
APPDATA = f"{str(os.environ.get('APPDATA'))}\\{PYTIA}\\{PYTIA_QUICK_EXPORT}"
LOGS = f"{APPDATA}\\logs"
LOG = "app.log"
PID = os.getpid()
PID_FILE = f"{TEMP}\\{PYTIA_QUICK_EXPORT}.pid"
VENV = f"\\.env\\{APP_VERSION}"
VENV_PYTHON = VENV + "\\Scripts\\python.exe"
VENV_PYTHONW = VENV + "\\Scripts\\pythonw.exe"
PY_VERSION = APPDATA + "\\pyversion.txt"

CONFIG_APPDATA = "config.json"
CONFIG_SETTINGS = "settings.json"
CONFIG_KEYWORDS = "keywords.json"
CONFIG_DEPS = "dependencies.json"
CONFIG_DEPS_DEFAULT = "dependencies.default.json"
CONFIG_EXCEL = "excel.json"
CONFIG_EXCEL_DEFAULT = "excel.default.json"
CONFIG_PROPS = "properties.json"
CONFIG_PROPS_DEFAULT = "properties.default.json"
CONFIG_USERS = "users.json"
CONFIG_DOCKET = "docket.json"

PROP_DRAWING_PATH = "pytia.drawing_path"

TEMPLATE_DOCKET = "docket.CATDrawing"
TEMPLATE_MAIL = "mail.html"

WEB_PIP = "www.pypi.org"

KEEP = "Keep"


os.makedirs(TEMP_EXPORT, exist_ok=True)
os.makedirs(TEMP_ATTACHMENTS, exist_ok=True)
os.makedirs(TEMP_TEMPLATES, exist_ok=True)
