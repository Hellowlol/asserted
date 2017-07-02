import datetime
import os
import logging
import sys

try:
    import asyncio
except ImportError:
    pass

import pytest

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


from .conftest import asserted


if sys.version_info >= (3, 4):
    @asyncio.coroutine
    async def hey():
        return 'hey'

    def test_hey(tmpdir):
        assert asserted.assert_writer(hey, fixups=[('hey', '', lambda k:k.upper())],
                                      save_path=str(tmpdir)) == ['hey = await hey.hey()\n        assert hey == "HEY"']


def hello():
    return 'is it me your looking for?'


def test_asserted(tmpdir):
    asserted.assert_writer(asserted.example_class.Ex(), write_full_tests=True,
                           save_path=str(tmpdir), sort_iterables=True)


def test_asserted_as_function(tmpdir):
    r = asserted.assert_writer(hello, write_full_tests=True, save_path=str(tmpdir))
    assert r == """def test_hello():
    hello = hello
    assert hello.hello() == "is it me your looking for?"
"""

# This is the what test_asserted writes to files.
# find a way to test that dynamically.
def test_ex():
    ex = asserted.example_class.Ex()
    assert ex.a_classmethod() == "a_classmethod"
    assert sorted(list(ex.a_generator_function())) == [0, 1, 2]
    assert ex.a_staticmethod() == "a_staticmethod"
    assert ex.att1 == "att1"
    assert ex.data == "data"
    assert str(ex.is_datetime.date()) == "1970-01-01"
    assert sorted(ex.is_dict.items()) == [('a', 'a'), ('b', 'b')]
    assert ex.is_float == 0.5
    assert sorted(list(ex.is_generator_expression)) == [0, 1]
    assert ex.is_int == 1
    assert sorted(ex.is_list) == [1, 2, 3, 4, 5]
    assert sorted(ex.is_tuple) == [1, 2, 3]
    assert ex.method() == "method"
    assert ex.props == "props"

    async def gogo():
        a_coro_with_return = await ex.a_coro_with_return()
        assert a_coro_with_return == "a_coro_with_return"
        async_metod = await ex.async_metod()
        assert async_metod == "async_metod"
        async_metod_two = await ex.async_metod_two()
        assert async_metod_two == "async_metod_two"
    asyncio.get_event_loop().run_until_complete(gogo())
