import sys
import os
import logging

import datetime

import asyncio

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


from .conftest import asserted


def hello():
    return 'is it me your looking for?'


def test_asserted(tmpdir):
    asserted.assert_writer(asserted.example_class.Ex(), write_full_tests=True, save_path=str(tmpdir))


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
    assert list(ex.a_generator_function()) == [0, 1, 2]
    assert ex.a_staticmethod() == "a_staticmethod"
    assert ex.att1 == "att1"
    assert ex.data == "data"
    assert str(ex.is_datetime.date()) == "1970-01-01"
    assert ex.is_dict == {}
    assert ex.is_float == 0.5
    assert list(ex.is_generator_expression) == [0, 1]
    assert ex.is_int == 1
    assert ex.is_list == []
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
