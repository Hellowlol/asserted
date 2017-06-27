from sys import version_info

PY34 = version_info >= (3, 4) and version_info < (3, 5)
PY35 = version_info >= (3, 5)


import inspect


if PY34:
    inspect.isawaitable = lambda k: False
    inspect.iscoroutine = lambda k: False
    inspect.iscoroutinefunction = lambda k: False
