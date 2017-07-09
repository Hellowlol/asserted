import argparse
import logging
import re

from asserted.utils import loader, REG_CLASS, REG_FUNC, TO_REMOVE
from asserted import assert_writer


def get_args():

    parser = argparse.ArgumentParser(description='A simple tool to write tests for pytest.')

    parser.add_argument('fp', help='The file you want to write test for.')

    parser.add_argument('-oa', '--only_attributes', action='store_false', default=False,
                        help='Only assert attributes, skip methods.')

    parser.add_argument('-wf', '--write_full_tests', action='store_true', default=True,
                        help='Write a test suite for fp')

    parser.add_argument('-tp', '--test_prefix', action='store_false', default='test_',
                        help='Prefix for tests. This is used by pytest to pickup the tests-')

    parser.add_argument('-sp', '--save_path', default='',
                        help='Where to save the output of the test.')

    parser.add_argument('-sm', '--separate_methods', action='store_true', default=True,
                        help='Separate methods to there own test functions.')

    parser.add_argument('-st', '--sort_iterables', action='store_true', default=False,
                        help='Sort interables to ensure test consistency')
    parser.add_argument('-q', action='store_true', default=False,
                        help='Disable logging.')

    n = parser.parse_args()

    params = vars(n)
    fp = params.pop('fp')
    quiet = params.pop('q')
    if quiet is False:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

    return params, fp


def get_stuff_to_assert(fp):

    with open(fp) as f:
        for i, line in enumerate(f.readlines(), 1):
            a_class = REG_CLASS.match(line)
            a_func = REG_FUNC.match(line)

            if a_func or a_class:
                d = {'path': fp,
                     'line': i,
                     'match': '',
                     'type': ''}

                if a_func:
                    d['type'] = 'func'
                    d['match'] = re.sub(TO_REMOVE, '', a_func.group(1))
                elif a_class:
                    m = re.sub(TO_REMOVE, '', a_class.group(1))
                    d['type'] = 'class'
                    d['match'] = m

                yield d


def run(d, params):
    m = loader(d['path'])

    class_or_func = getattr(m, d.get('match'))

    # We can use inspect for this for this. Lets just keep it for now
    if d.get('type') == 'class':
        class_or_func = class_or_func()
        assert_writer(class_or_func, caller_name='%s()' % class_or_func.__class__.__name__, **params)

    elif d.get('type') == 'func':
        assert_writer(class_or_func, caller_name='%s()' % class_or_func.__name__, **params)


def main():
    params, fp = get_args()

    for item in get_stuff_to_assert(fp):
        run(item, params)


if __name__ == '__main__':
    main()
