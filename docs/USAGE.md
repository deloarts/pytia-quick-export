# usage

> ✏️ This covers the usage of the app, which depends on the configuration of the `settings.json` config file. If you use different names for properties or disable some of the functionality, the apps layout may be different from the one in this guide.

- [usage](#usage)
  - [1 launcher](#1-launcher)
  - [2 app](#2-app)

## 1 launcher

If your setup is done (see [installation](./INSTALLATION.md)), open the app from within CATIA. If this is the first time, you'll see the launcher will install all necessary dependencies:

![Installer](/assets/images/installer.png)

After the installation you can run the app.

## 2 app

The usage itself is pretty straight forward, as long as all config files are setup properly.

![App](/assets/images/app.png)

The usage itself is pretty straight forward, as long as all config files are setup properly.

Object | Description
--- | ---
Project | The user can overwrite the project number for all items of the bill of material. If set to `Keep` no project number will be overwritten.
Condition | The condition of the document. Can be `new` or `modification`. New means, that the part needs to be made, modification means that a parts need to be modified (maybe due to a revision).
Quantity | The amount of parts to make.
Note | A note for the export. Will only be displayed in the mail body and nowhere else.
Mail Address | The receiver of the exported files.
Export Folder | The location to which the data will be written.

To enable the export, you have to provide a mail address or the export folder, or both.
