from .conftest import asserted


def test_indent():
    pass


def test_wrap_in_asunc_func():
    pass


def test_check_value():
    assert asserted.utils.check_value('hello') == '"hello"'
    assert asserted.utils.check_value(1) == 1


def test_test_writer():
    pass


def test_get_caller():
    pass


def test_get_value():
    pass
    #assert asserted.utils.get_value('hello', 'z') == '"hello"'
    #assert asserted.utils.get_value(1, '') == 1



def test_internals():
    class T():
        def __init__(self):
            self.a = 'a'
            self.b = 'b'
            self._p = '_p'

        def c(self):
            return

    assert asserted.utils.internals(T(), only_attributes=True) == ['a', 'b']
    assert asserted.utils.internals(T(), only_attributes=False) == ['a', 'b', 'c']
    assert asserted.utils.internals(T(), only_attributes=False, include_private=True) == ['_p', 'a', 'b', 'c']
