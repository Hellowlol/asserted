import asyncio
import os
import logging
import re

from .compat import *

LOG = logging.getLogger(__name__)


def indent(text, char=' ', indentation=4, new_line=True):
        padding = char * indentation
        if new_line:
            return '\n'.join(padding + line for line in text)
        else:
            return ''.join(padding + line for line in text)


def wrap_in_asunc_func(v):
    x = '\n    async def gogo():\n%s\n    asyncio.get_event_loop().run_until_complete(gogo())' % v

    return x


def call_until_exhausted(value, item):
    """"""
    loop = asyncio.get_event_loop()
    was_async = False

    async def coro(hello):
        return await hello

    if inspect.ismethod(value):
        value = value()

    while inspect.isawaitable(value):
        value = loop.run_until_complete(coro(value))
        was_async = True

    return value, was_async


def check_value(value):
    """Makes sure we quote what we need correctly."""
    if isinstance(value, str):
        value = '"%s"' % value
    elif isinstance(value, int):
        value = value

    return value


def test_writer(test_prefix, name, caller, results, results_async=''):
    """Template for the test."""
    result = indent(results, new_line=True)

    if results_async:
        results_async = indent(results_async, new_line=True, indentation=8)
        results_async = wrap_in_asunc_func(results_async)
    else:
        results_async = ''
    s = "def %s%s():\n    %s\n%s\n%s" % (test_prefix, name, caller, result, results_async)
    return s


def get_caller(f, ln):
    LOG.debug('Checking %s line %s to find what assertwriter was called with' % (f, ln))
    kek = None
    with open(os.path.abspath(f)) as f:
        for i, line in enumerate(f.readlines(), 1):
            if i == ln:

                kek = re.search('assert_writer\(([^,]*)', line)
                if kek:
                    kek = kek.group(1)
                    break

    return kek


def get_value(func, item, limit_to_one_value=False):
    """Get result from the attr call and if it required a async call."""

    name = func.__class__.__name__
    name = '%s.%s' % (name, item)
    was_async = False
    value = getattr(func, item)

    if PY35:
        value, was_async = call_until_exhausted(value, item)

    if callable(value):
        value = value()

    LOG.debug('Value for %s is %s' % (name, value))
    return value, was_async


def internals(func, only_attributes=True, include_private=False):
    """Returns attributes and/or methods."""

    if only_attributes:
        attrs = sorted(vars(func))
    else:
        attrs = sorted(dir(func))

    filter_attrs = []
    for at in attrs:
        if at.endswith('__'):
            continue
        if not include_private and at.startswith('_'):
            continue
        else:
            filter_attrs.append(at)

    return filter_attrs
