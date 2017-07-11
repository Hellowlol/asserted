import os
import pytest

from .conftest import PATH, cli

pytest_plugins = ["pytester"]


def test_cli(tmpdir, path):
    f = os.path.join(str(PATH), 'asserted', 'example_class.py')
    print('fuck', f)

    d = {'write_full_tests': True,
         'save_path': path,
         'separate_methods': True,
         'sort_iterables': True}

    cli.main((d, f))
