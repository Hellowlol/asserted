import os
import sys

import pytest

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
HERE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'txt'))

sys.path.insert(0, PATH)

import asserted
from asserted import example_class


def pytest_addoption(parser):
    parser.addoption("--dev", action="store_true", default=False,
                     help="Write new txt files")


@pytest.fixture
def path(request, tmpdir):
    return HERE if request.config.getoption("--dev") else str(tmpdir)


@pytest.fixture
def run_cli(testdir):
    def run(*args):
        # taken from https://stackoverflow.com/questions/13493288/python-cli-program-unit-testing
        cli_path = os.path.join(PATH, 'asserted', 'cli.py')
        args = [sys.executable, cli_path] + list(args)
        return testdir._run(*args)

    return run
