"""
    Releases the app to the specified folder.
"""

import json
import os
import shutil

from pytia_quick_export.const import APP_NAME, APP_VERSION

with open("./pytia_quick_export/resources/settings.json", "r") as f:
    settings = json.load(f)

source_app = f"./build/{settings['files']['app']}"
source_launcher = f"./build/{settings['files']['launcher']}"
target_app = f"{settings['paths']['release']}/{settings['files']['app']}"
target_launcher = f"{settings['paths']['release']}/{settings['files']['launcher']}"


def move():
    if os.path.exists(source_app) and os.path.exists(source_app):
        shutil.move(source_app, target_app)
        shutil.move(source_launcher, target_launcher)
        print(f"App released to {settings['paths']['release']}")
    else:
        print("Failed: No build file.")


if __name__ == "__main__":
    print(f"Releasing {APP_NAME} {APP_VERSION}\n")
    move()
