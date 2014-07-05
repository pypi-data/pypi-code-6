try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
import sys

import pytest


def run_tests(path):
    # redirect stdout to grab return of pytest
    old_stdout = sys.stdout
    sys.stdout = new_stdout = StringIO()

    retcode = pytest.main(path)

    # restore stdout
    sys.stdout = old_stdout

    # get the number of tests run from pytest output
    ran = int(new_stdout.getvalue().split('collected ')[1][0])

    if retcode == 0:
        return (True, ran, 0)

    # get the number of failures from pytest output
    failures = int(new_stdout.getvalue().split(' failed')[0][-1])
    return (False, ran, failures)
