#
# lets just hack it for now..

import logging
import os
import re
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


from asserted.utils import REG_CLASS, REG_FUNC, loader
from asserted import assert_writer

def get_stuff_to_assert(fp):
    to_remove = re.compile('(\(.*?\))')
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
                    d['match'] = re.sub(to_remove, '', a_func.group(1))
                elif a_class:
                    m = re.sub(to_remove, '', a_class.group(1))
                    d['type'] = 'class'
                    d['match'] = m

                yield d



def run(d, params):
    # 3.4
    # https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    from importlib.machinery import SourceFileLoader

    m = loader(d['path'])#SourceFileLoader(os.path.basename(d['path']), d['path']).load_module()

    class_or_func = getattr(m, d.get('match'))

    if d.get('type') == 'class':
        class_or_func = class_or_func()
        assert_writer(class_or_func, write_full_tests=True, caller_name='%s()' % class_or_func.__class__.__name__, **params)

    elif d.get('type') == 'func':
        assert_writer(class_or_func, write_full_tests=True, caller_name='%s()' % class_or_func.__name__, **params)



def get_args():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('fp')

    parser.add_argument('-ip', action='store_false', default=False,
                        help='include private attributes/methods')
    parser.add_argument('-oa', action='store_false', default=False,
                        help='only attributes')
    parser.add_argument('-wf', action='store_true', default=True,
                        help='write tests')
    parser.add_argument('-tp', action='store_false', default='test_',
                        help='test prefix')
    parser.add_argument('-sp', action='store_false', default='',
                        help='savepath')

    n = parser.parse_args()

    params = vars(n)
    print(params)
    return n, params



def main():



    args, params = get_args()
    fp = r'C:\Users\alexa\OneDrive\Dokumenter\GitHub\asserted\asserted\example_class.py'

    # Lets hardcode for now..


    result = list(get_stuff_to_assert(fp))

    for res in result:
        run(res, params)




if __name__ == '__main__':
    main()
