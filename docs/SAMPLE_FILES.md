# sample files

Explains the config of all sample files.

All sample files must be copied, renamed and edited to fit your needs.

## 1 settings.sample.json

This file contains the basic settings for the app.

- **Location**: [/pytia_quick_export/resources/settings.sample.json](../pytia_quick_export/resources/settings.sample.json)
- **Rename to**: `settings.json`

### 1.1 file content

```json
{
    "title": "PYTIA Quick Export",
    "debug": false,
    "restrictions": {
        "allow_all_users": true,
        "allow_all_editors": true,
        "allow_unsaved": true,
        "allow_outside_workspace": true,
        "strict_project": true
    },
    "export": {
        "apply_username": true,
        "lock_drawing_views": true
    },
    "condition": {
        "new": {
            "name": "New"
        },
        "mod": {
            "name": "Modification",
            "overwrite": {
                "pytia.base_size": "Modification",
                "pytia.process_1": "Milling",
                "pytia.note_process_1": "Due to a modification, part is supplied.",
                "pytia.process_2": "",
                "pytia.note_process_2": "",
                "pytia.process_3": "",
                "pytia.note_process_3": "",
                "pytia.process_4": "",
                "pytia.note_process_4": "",
                "pytia.process_5": "",
                "pytia.note_process_5": "",
                "pytia.process_6": "",
                "pytia.note_process_6": ""
            }
        }
    },
    "paths": {
        "catia": "C:\\CATIA\\V5-6R2017\\B27",
        "release": "C:\\pytia\\release"
    },
    "files": {
        "app": "pytia_quick_export.pyz",
        "launcher": "pytia_quick_export.catvbs",
        "workspace": "workspace.yml"
    },
    "urls": {
        "help": null
    },
    "mails": {
        "subject": "New Export",
        "admin": "admin@company.com",
        "export": [
            "request@company.com"
        ],
        "export_debug": "dev@company.com"
    }
}
```

### 1.2 description

name | type | description
--- | --- | ---
title | `str` | The apps title. This will be visible in the title bar of the window.
debug | `bool` | The flag to declare the debug-state of the app. The app cannot be built if this value is true.
restrictions.allow_all_users | `bool` | If set to `true` any user can make changes to the documents properties. If set to `false` only those users from the **users.json** file can modify the properties.
restrictions.allow_all_editors | `bool` | If set to `true` any user can make changes to the documents properties. If set to `false` only those users which are declared in the **workspace** file can modify the properties. If no workspace file is found, or no **editors** list-item is inside the workspace file, then this is omitted, and everyone can make changes.
restrictions.allow_unsaved | `bool` | If set to `false` an unsaved document (a document which doesn't have a path yet) cannot be modified.
restrictions.allow_outside_workspace | `bool` | If set to `false` a **workspace** file must be provided somewhere in the folder structure where the document is saved. This also means, that an unsaved document (a document which doesn't have a path yet) cannot be modified.
restrictions.strict_project | `bool` | If set to `true` the project number must be present in the **workspace** file, otherwise the changes to the properties cannot be saved. If no workspace file is found, or no **projects** list-item is inside the workspace file, then this is omitted, and any project number can be written to the documents properties.
export.apply_username | `bool` | Whether to translate the username or not.
export.lock_drawing_views | `bool` | Whether to lock all drawing views after the export or not.
condition.new.name | `str` | The name of the condition 'new'. This is more an option if you don't want to use english words on the docket or in the Excel file.
condition.mod.name | `str` | The name of the condition 'modification'.
condition.mod.overwrite | `Dict[str]` | An dict-object that holds all property names as keys and the property values as values, which are going to be overwritten when the condition is 'modification'.<br><br>Example: When the condition is 'modification', you don't want a part to have all process steps, you only want it to be milled as first process. This case is shown in the sample file.
paths.catia | `str` | The absolute path to the CATIA executables.
paths.release | `str` | The folder where the launcher and the app are released into.
file.bom_export | `str` | The standard name for the final bill of material. If a bom_name is set in the **workspace** file, the workspace-bom-name will be used.
files.app | `str` | The name of the released python app file.
files.launcher | `str` | The name of the release catvbs launcher file.
files.workspace | `str` | The name of the workspace file.
urls.help | `str` or `null` | The help page for the app. If set to null the user will receive a message, that no help page is provided.
mail.subject | `str` | The subject of the mail (the project number will be prefixed).
mails.admin | `str` | The mail address of the sys admin. Required for error mails.
mails.export | `List[str]` | The email addresses which will be available in the UI for the export.
mail.export_debug | `str` | The mail address you can use while debugging the app. This will be used when `debug` is set to `true`.

## 2 users.sample.json

This file contains a list of users known to the system.

- **Location**: [/pytia_quick_export/resources/users.sample.json](../pytia_quick_export/resources/users.sample.json)
- **Rename to**: `users.json`

### 2.1 file content

```json
[
    {
        "logon": "admin",
        "id": "001",
        "name": "Administrator",
        "mail": "admin@company.com"
    },
    ...
]
```

### 2.2 description

name | type | description
--- | --- | ---
logon | `str` | The windows logon name of the user.
id | `str` | The ID of the user. Can be used for the employee ID.
name | `str` | The name of the user.
mail | `str` | The users mail address.

## 3 docket.sample.json

This file contains the configuration for the docket export.

> ⚠️ This config file will be documented later, as the docket generation will be changed in the future (it's currently a very hacky solution).

- **Location**: [/pytia_quick_export/resources/docket.sample.json](../pytia_quick_export/resources/users.sample.json)
- **Rename to**: `docket.json`
