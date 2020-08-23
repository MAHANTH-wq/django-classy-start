import pathlib
import shlex

import mock

from classy_start.paths import APP_TEMPLATES_DIR, PROJECT_TEMPLATES_DIR
from classy_start.start import (
    start_app,
    start_project,
    follow_up_start_project,
    rename_file,
)


def test_start_app(fake_process):

    fake_process.keep_last_process(True)
    fake_process.register_subprocess([fake_process.any()])

    start_app("appify")

    count = fake_process.call_count(
        shlex.split(f"django-admin startapp appify --template '{APP_TEMPLATES_DIR!s}'")
    )
    assert count == 1


@mock.patch("classy_start.start.follow_up_start_project")
def test_start_project(mock_follow_up, fake_process):

    fake_process.keep_last_process(True)
    fake_process.register_subprocess([fake_process.any()])

    start_project("projectible", ".")

    count = fake_process.call_count(
        shlex.split(
            f"django-admin startproject projectible . --template '{PROJECT_TEMPLATES_DIR!s}'"
        )
    )
    assert count == 1

    mock_follow_up.assert_called_once_with("projectible", ".")


@mock.patch("pathlib.Path.resolve")
@mock.patch("classy_start.start.rename_file")
def test_follow_up_start_project(mock_rename_file, _mock_resolve):
    """
    Assert that ~.follow_up_start_project() calls ~.rename_file() the correct number of
    times and with the correct arguments.
    """
    follow_up_start_project("projectible")

    assert mock_rename_file.call_count == 3
    mock_rename_file.assert_has_calls(
        [
            mock.call("secrets.py", ".env", base_dir=pathlib.Path("projectible")),
            mock.call(
                "gitignore.py", ".gitignore", base_dir=pathlib.Path("projectible")
            ),
            mock.call(
                "requirements.py",
                "requirements.txt",
                base_dir=pathlib.Path("projectible"),
            ),
        ]
    )

    mock_rename_file.reset_mock()
    follow_up_start_project("projectible", pathlib.Path("."))

    assert mock_rename_file.call_count == 3
    mock_rename_file.assert_has_calls(
        [
            mock.call("secrets.py", ".env", base_dir=pathlib.Path(".")),
            mock.call("gitignore.py", ".gitignore", base_dir=pathlib.Path(".")),
            mock.call(
                "requirements.py", "requirements.txt", base_dir=pathlib.Path("."),
            ),
        ]
    )


@mock.patch("pathlib.Path.rename")
def test_rename_file(mock_rename):
    """
    Assert that ~.rename_file() calls pathlib.Path.rename with the correct target.
    """
    base_dir = pathlib.Path(".") / "projectible"
    rename_file("old_name", "new_name", base_dir)

    mock_rename.assert_called_once_with(base_dir / "new_name")
