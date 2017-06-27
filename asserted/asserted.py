import datetime
import logging

from .utils import *
from .compat import *

__all__ = ['assert_writer']


LOG = logging.getLogger(__name__)


def assert_writer(func, fn=None, include_private=False, only_attributes=False,
                  write_full_tests=False, test_prefix='test_', save_path='', fixups=None, unpack_iterables=False):
    """Simple assert helper that takes automates some of the
       boiler plate when writing unit tests for pytest

       Args:
            func (callable): The object you want asserted
            fn (func): filename
            include_private(bool): assert private vars too
            only_attributes(bool): Only add asserts with the attrs
            write_full_tests(bool): for simple copypasta
            save_path (string): default None
            test_prefix(str): Default test_
            fixups(list): [('file_path', 'os.path.basename', os.path.basename)]

    """
    # Lets see if func belongs to a class. If not we are gonna add it to a class.
    if func.__class__.__name__ == 'function': # Please find a better way..
        LOG.debug('Created parent class %s' % func.__name__)
        func = type(func.__name__, (object,), {func.__name__: func})

    if fixups is None:
        fixups = []

    if not save_path:
        save_path = os.path.expanduser('~/asserted')
        # no exists on py2.
        try:
            os.makedirs(save_path)
        except OSError:
            if not os.path.isdir(save_path):
                raise

    result = []
    result_async = []

    if PY35 and inspect.isawaitable(func):
        loop = asyncio.get_event_loop()
        LOG.debug('%s is awaitable executing in eventloop' % func)
        func = loop.run_until_complete(func)

    try:
        org_name = func.__class__.__name__.lower()
    except AttributeError:
        # Normal functions isnt suppored at TODO
        org_name = func.__name__.lower()

    attrs = internals(func, include_private=include_private,
                      only_attributes=only_attributes)

    for item in attrs:
        assert_line = ''
        variable_name = '%s.%s' % (org_name, item)

        value, was_async = get_value(func, item)

        cld = getattr(func, item)

        # Make the variable_name callable
        if callable(cld):
            variable_name = '%s()' % variable_name

        # Fix the value and eq
        eq = '=='
        value = check_value(value)
        if isinstance(value, bool):
            eq = 'is'

        # lets fixup datetimes since they are rather common.
        if isinstance(value, datetime.datetime):
            variable_name = 'str(%s.date())' % variable_name
            value = '"%s"' % value.date()

        elif inspect.isgenerator(value) and not inspect.isawaitable(value):
            value = list(value)
            variable_name = 'list(%s)' % variable_name

        # Handle overrides..
        if fixups:
            for fix in fixups:
                if fix[0] == item:
                    variable_name = "%s(%s)" % (fix[1], variable_name)
                    value = "'%s'" % fix[2](value)

        # Final assert line
        assert_line = "assert %s %s %s" % (variable_name, eq, value)

        if (inspect.isawaitable(cld) or inspect.iscoroutine(cld) or
            inspect.iscoroutinefunction(cld) or was_async):

            assert_line = '%s = await %s\n%sassert %s %s %s' % (item, variable_name, ' ' * 8, item, eq, value)
            result_async.append(assert_line)
        else:
            result.append(assert_line)

    if write_full_tests:
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        # Extract the code that was passed as
        # func from the source code.
        func_call_name = get_caller(caller.filename, caller.lineno)
        # Make the first assert line
        called_with = '%s = %s' % (org_name, func_call_name)
        t = test_writer(test_prefix, org_name, called_with, result, result_async)
        fn = os.path.join(save_path, '%s_func.txt' % org_name)
        with open(fn, 'w') as file:
            file.write(t)
            LOG.info('All done. Wrote %s to disks' % os.path.abspath(fn))
        return

    if fn:
        fn = '%s.txt' % org_name
        with open(fn, 'a') as file:
            file.write('    \n'.join(result))

    return result