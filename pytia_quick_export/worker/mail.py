"""
    Mail export task.
"""
from datetime import datetime
from pathlib import Path
from shutil import make_archive

import jinja2
from helper.outlook import get_outlook
from pytia.exceptions import PytiaApplicationError
from templates import templates


def export_mail(
    project: str,
    machine: str,
    partnumber: str,
    revision: str,
    condition: str,
    quantity: str,
    note: str,
    receiver: str,
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

    mail = outlook.CreateItem(0)
    mail.To = receiver
    mail.Subject = f"{project} | {machine} {partnumber} Rev{revision}"
    mail.HTMLBody = _render_template(
        project=project,
        machine=machine,
        partnumber=partnumber,
        revision=revision,
        condition=condition,
        quantity=quantity,
        note=note if len(note) > 0 else "-",
    )

    archive = make_archive(
        base_name=str(
            Path(
                attachments_folder,
                f"{project}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}",
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
