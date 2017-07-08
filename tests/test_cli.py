import os
import pytest

from .conftest import PATH

pytest_plugins = ["pytester"]


def test_cli(run_cli, tmpdir, path):
    f = os.path.join(str(PATH), 'asserted', 'example_class.py')
    run_cli(f, '-sp', path)
