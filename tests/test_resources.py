"""
    Test the resources.py file.
"""

import os

import validators


def test_resources_class():
    from pytia_quick_export.resources import Resources

    resource = Resources()


def test_settings():
    from pytia_quick_export.resources import resource

    # TODO


def test_users():
    from pytia_quick_export.resources import resource

    logon_list = []

    for user in resource.users:
        assert isinstance(user.logon, str)
        assert isinstance(user.id, str)
        assert isinstance(user.name, str)
        assert isinstance(user.mail, str)
        assert user.logon not in logon_list

        logon_list.append(user.logon)


def test_release_folder():
    from pytia_quick_export.resources import resource

    assert os.path.isdir(resource.settings.paths.release)


def test_debug_mode():
    from pytia_quick_export.resources import resource

    assert resource.settings.debug == False
