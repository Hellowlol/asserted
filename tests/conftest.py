import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.insert(0, path)

HERE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'txt'))

import asserted
from asserted import example_class

import pytest


def pytest_addoption(parser):
    parser.addoption("--dev", action="store_true", default=False,
                     help="Write new txt files")

@pytest.fixture
def dev(request, tmpdir):
    return HERE if request.config.getoption("--dev") else str(tmpdir)
