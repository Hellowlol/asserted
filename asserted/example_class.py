import asyncio
import datetime


class Ex:
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
