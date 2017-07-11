import pytest

from .conftest import asserted

TODO = pytest.mark.skip(reason="Not implemented")


class T():
    def __init__(self):
        self.a = 'a'
        self.b = 'b'
        self._p = '_p'

    def c(self):
        return


@TODO
def test_loader():
    pass


def test_indent():
    assert asserted.utils.indent(['a']) == '    a'
    assert asserted.utils.indent(['b'], new_line=False) == '    b'


@TODO
def test_wrap_in_asunc_func():
    pass


def test_check_value():
    assert asserted.utils.check_value('hello') == '"hello"'
    assert asserted.utils.check_value(1) == 1


@TODO
def test_test_writer():
    pass


@TODO
def test_get_caller():
    pass


def test_get_value():
    assert asserted.utils.get_value(T(), 'a') == ('a', False)
    assert asserted.utils.get_value(T(), 'c') == (None, False)


def test_internals():
    assert asserted.utils.internals(T(), only_attributes=True) == ['a', 'b']
    assert asserted.utils.internals(T(), only_attributes=False) == ['a', 'b', 'c']
    assert asserted.utils.internals(T(), only_attributes=False, include_private=True) == ['_p', 'a', 'b', 'c']
