import os
import sys

import pytest

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
HERE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'txt'))

sys.path.insert(0, PATH)

import asserted
from asserted import cli, example_class


def pytest_addoption(parser):
    parser.addoption("--dev", action="store_true", default=False,
                     help="Write new txt files")


@pytest.fixture
def path(request, tmpdir):
    return HERE if request.config.getoption("--dev") else str(tmpdir)
