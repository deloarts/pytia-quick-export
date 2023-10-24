"""
    Mail export task.
"""
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from shutil import make_archive

import jinja2
from helper.outlook import get_outlook
from models.data import DataModel
from models.data import DatumModel
from pytia.exceptions import PytiaApplicationError
from resources import resource
from templates import templates


def export_mail(
    data: DataModel,
    selected_project: str,
    selected_condition: str,
    selected_receiver: str,
    note: str,
    attachments_folder: Path,
    data_folder: Path,
) -> None:
    """Composes an email.

    Raises:
        PytiaApplicationError: Raised when no connection to the local outlook app can be established
    """
    outlook = get_outlook()
    if outlook is None:
        raise PytiaApplicationError("Outlook is not available on this machine.")

    mail = outlook.CreateItem(0)  # FIXME: This fails if Outlook isn't running
    mail.To = selected_receiver
    mail.Subject = f"{selected_project} | {resource.settings.mails.subject}"
    mail.HTMLBody = _render_template(
        data=data.data,
        settings=resource.settings,
        condition=selected_condition,
        note=note,
    )

    archive = make_archive(
        base_name=str(
            Path(
                attachments_folder,
                f"{selected_project}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}",
            )
        ),
        format="zip",
        root_dir=str(data_folder),
    )
    mail.Attachments.Add(archive)
    mail.Display()


def _render_template(**kwargs) -> str:
    """Renders the template."""
    if templates.mail_path is None:
        return "Template file is missing."

    loader = jinja2.FileSystemLoader(templates.mail_path.parent)
    env = jinja2.Environment(loader=loader)
    template = env.get_template(templates.mail_path.name)
    return template.render(**kwargs)
