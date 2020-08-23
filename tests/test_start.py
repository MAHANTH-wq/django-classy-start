import shlex

from classy_start.paths import APP_TEMPLATES_DIR, PROJECT_TEMPLATES_DIR
from classy_start.start import start_app, start_project


def test_start_app(fake_process):

    fake_process.keep_last_process(True)
    fake_process.register_subprocess([fake_process.any()])

    start_app("appify")

    count = fake_process.call_count(
        shlex.split(f"django-admin startapp appify --template '{APP_TEMPLATES_DIR!s}'")
    )
    assert count == 1


def test_start_project(fake_process):

    fake_process.keep_last_process(True)
    fake_process.register_subprocess([fake_process.any()])

    start_project("projecterize", ".")

    count = fake_process.call_count(
        shlex.split(
            f"django-admin startproject projecterize . --template '{PROJECT_TEMPLATES_DIR!s}'"
        )
    )
    assert count == 1
