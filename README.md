# asserted
[![Travis Status](https://travis-ci.org/Hellowlol/asserted.svg?branch=master)](https://travis-ci.org/Hellowlol/asserted)
[![Cov](https://codecov.io/gh/hellowlol/asserted/branch/master/graph/badge.svg)](https://codecov.io/gh/hellowlol/asserted/branch/master)
[![GitHub Releases](https://img.shields.io/github/tag/hellowlol/asserted.svg?label=github+release)](https://github.com/hellowlol/asserted/releases)
[![PyPI version](https://badge.fury.io/py/asserted.svg)](https://pypi.python.org/pypi/asserted/)

asserted is a simple tool that writes a pytest for the object your pass to it.
This is no way near perfect, you still have to handle imports, fixtures at but its handy if you need to check that all the properties are correct.

#### CLI:
asserted path/to/file
use -h to see all the options.


#### Code:
Say you have a class like:
````
class Ex(object):
    def __init__(self):
        self.data = 'data'
        self.att1 = 'att1'
        self.is_list = []
        self.is_dict = {}
        self.is_int = 1
        self.is_float = 0.5
        self.is_generator_expression = (i for i in range(2))
        self.is_datetime = datetime.datetime(1970, 1, 1)

    @property
    def props(self):
        """Comment"""
        return 'props'

    def method(self):
        return 'method'

    async def async_metod(self):
        return 'async_metod'

    async def async_metod_two(self):
        return 'async_metod_two'

    @classmethod
    def a_classmethod(cls):
        return 'a_classmethod'

    @staticmethod
    def a_staticmethod():
        return 'a_staticmethod'

    @asyncio.coroutine
    def a_coro_with_return(self):
        return 'a_coro_with_return'

    def a_generator_function(self):
        for i in range(3):
            yield i

    def a_missing_arg(self, arg):
        return arg
````


````
assert_write(asserted.example_class.Ex(), write_full_tests=True, separate_methods=True, sort_iterables=True)  #  will create a this file:

def test_ex():
    ex = asserted.example_class.Ex()
    assert ex.att1 == "att1"
    assert ex.data == "data"
    assert str(ex.is_datetime.date()) == "1970-01-01"
    assert sorted(ex.is_dict.items()) == [('a', 'a'), ('b', 'b')]
    assert ex.is_false is False
    assert ex.is_float == 0.5
    assert sorted(list(ex.is_generator_expression)) == [0, 1]
    assert ex.is_int == 1
    assert sorted(ex.is_list) == [1, 2, 3, 4, 5]
    assert ex.is_true is True
    assert sorted(ex.is_tuple) == [1, 2, 3]
    assert ex.props == "props"

def test_ex_classmethod():
    ex = asserted.example_class.Ex()
    assert ex.a_classmethod() == "a_classmethod"

def test_ex_coro_with_return():
    ex = asserted.example_class.Ex()

    async def gogo():
        a_coro_with_return = await ex.a_coro_with_return()
        assert a_coro_with_return == "a_coro_with_return"
    asyncio.get_event_loop().run_until_complete(gogo())

def test_ex_generator_function():
    ex = asserted.example_class.Ex()
    assert sorted(list(ex.a_generator_function())) == [0, 1, 2]

def test_ex_a_staticmethod():
    ex = asserted.example_class.Ex()
    assert ex.a_staticmethod() == "a_staticmethod"

def test_ex_async_metod():
    ex = asserted.example_class.Ex()

    async def gogo():
        async_metod = await ex.async_metod()
        assert async_metod == "async_metod"
    asyncio.get_event_loop().run_until_complete(gogo())

def test_ex_async_metod_two():
    ex = asserted.example_class.Ex()

    async def gogo():
        async_metod_two = await ex.async_metod_two()
        assert async_metod_two == "async_metod_two"
    asyncio.get_event_loop().run_until_complete(gogo())

def test_ex_method():
    ex = asserted.example_class.Ex()
    assert ex.method() == "method"

def test_ex_missing_a_arg():
    ex = asserted.example_class.Ex()
    assert ex.missing_a_arg() == "Missing_ARG"

````
