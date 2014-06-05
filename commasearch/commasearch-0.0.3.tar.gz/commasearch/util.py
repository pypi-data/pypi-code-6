import itertools
from io import StringIO
from traceback import print_exc

def traceback():
    not_file = StringIO()
    print_exc(file = not_file)
    return not_file.getvalue()

def column_combinations(colnames):
    return map(tuple, map(sorted, (itertools.chain(*(itertools.combinations(colnames, i) for i in range(1, len(colnames) + 1))))))
