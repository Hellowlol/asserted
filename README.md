# asserted

This is no way near perfect, you still have to handle imports, fixtures at but it handy if you need to check that all the properties are correct.


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
````
assert_write(Ex(), write_full_tests=True) will create a this file:

````
def test_ex():
    ex = Ex()
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
````
