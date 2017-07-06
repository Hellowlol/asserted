import asyncio
import os
import logging
import re

from .compat import *

LOG = logging.getLogger(__name__)
REG_CLASS = re.compile('^class\s(\w+\(?\w+?\)?):')
REG_FUNC = re.compile('^def\s(\w+\(?\)?):')


def loader(path):
    # https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    # fix me for compat
    from importlib.machinery import SourceFileLoader
    m = SourceFileLoader(os.path.basename(path), path).load_module()
    return m


def indent(text, char=' ', indentation=4, new_line=True):
        padding = char * indentation
        if new_line:
            return '\n'.join(padding + line for line in text)
        else:
            return ''.join(padding + line for line in text)


def wrap_in_asunc_func(v): # Change to coro
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

    if inspect.isfunction(value):
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
    LOG.debug('Writing test for %s' % name)
    result = indent(results, new_line=True)

    if results_async:
        results_async = indent(results_async, new_line=True, indentation=8)
        results_async = wrap_in_asunc_func(results_async)
    else:
        results_async = ''

    s = "def %s%s():\n    %s\n%s%s\n\n" % (test_prefix, name, caller, result, results_async)
    return s


def get_caller(f, ln):
    LOG.debug('Checking %s line %s to find what assert_writer was called with' % (f, ln))
    found = ''
    reg = re.compile('assert_writer\((.+)?\,?\)?')
    with open(os.path.abspath(f)) as f:
        lines = f.readlines()
        # We want to start from the ends since ln is the last line assert_writer was on.
        # Incase the it spanned over serveral lines.
        for line in reversed(lines[:ln + 1]):
            found = re.search(reg, line)
            if found:
                found = found.group(1)
                if ',' in found:
                    found = found.split(',')[0]

                found = found.strip()
                break
    LOG.debug('assert_writer was called with %s' % found)
    return found


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
        elif not include_private and at.startswith('_'):
            continue
        else:
            filter_attrs.append(at)

    return filter_attrs
