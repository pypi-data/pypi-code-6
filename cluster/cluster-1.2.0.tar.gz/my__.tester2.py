from __future__ import print_function
from collections import namedtuple
from cluster import HierarchicalClustering
from difflib import SequenceMatcher


def sim(x, y):
    sm = SequenceMatcher(lambda x: x in ". -", x, y)
    return 1 - sm.ratio()

data = ("Lorem ipsum dolor sit amet, consectetuer adipiscing "
        "elit. Ut elit. Phasellus consequat ultricies mi. Sed congue "
        "leo at neque. Nullam.").split()

data = [_.strip(',. ') for _ in data]


Cluster = namedtuple('C', 'l, v')
Element = namedtuple('E', 'i, v')


def run(data):
    "Basic Hierachical clustering test with strings"
    cl = HierarchicalClustering(data, sim)
    print(cl.getlevel(0.5))


def print_matrix(data):
    print(': '.join(data))
    for i, x in enumerate(data):
        sims = ['{:0.3f}'.format(sim(x, _)) for _ in data[:i]]
        print(x, ': '.join(sims), sep=': ')


## def matrix(data):
##     for i, x in enumerate(data):
##         for j, y in enumerate(data[:i]):
##             minsim = min([sim(ex.v, ey.v)
##                           for ex in x.v for ey in y.v])
##             yield Cluster(minsim, [Element(i, x), Element(j, y)])
##
##
## print(data)
## data = matrix([Cluster(-1, [Element(i, _)]) for i, _ in enumerate(data)])
## print(list(data)[0])
## print(80*'-')
## sorted_cells = sorted(data, key=lambda x: x.l)
## cluster = sorted_cells[0]
## print(cluster)
## print(80*'-')

# print_matrix(data)


data = [['Lorem'],
        ['ipsum'],
        ['dolor'],
        ['sit'],
        ['amet'],
        ['consectetuer'],
        ['adipiscing'],
        ['elit'],
        ['Ut'],
        ['elit'],
        ['Phasellus'],
        ['consequat'],
        ['ultricies'],
        ['mi'],
        ['Sed'],
        ['congue'],
        ['leo'],
        ['at'],
        ['neque'],
        ['Nullam']]


def matrix(data):
    for i, row in enumerate(data):
        for j, cell in enumerate(data[:i]):
            minsim = min([sim(ex, ey)
                          for ex in row for ey in cell])
            yield (minsim, (i, j))


def step(data):
    while len(data) > 1:
        sorted_matrix = sorted(matrix(data), key=lambda x: x[0])
        closest_items = sorted_matrix[0]
        a, b = closest_items[1]
        new_element = data.pop(max(a, b)) + data.pop(min(a, b))
        data.append(new_element)
        return data


def myminsim(a, b):
    return min([sim(ex, ey) for ex in a for ey in b])


def print_matrix2(data, iteration):
    print('.. csv-table:: Matrix #{}'.format(iteration))
    print('    :header-rows: 1')
    print('    :stub-columns: 1')
    print('    :delim: :\n')
    print('    :' + ': '.join([', '.join(_) for _ in data]))
    for i, row in enumerate(data):
        simdata = ['{:.3f}'.format(myminsim(row, x)) for x in data[:i]]
        print('    ' + ','.join(row), ': '.join(simdata), sep=': ')


i = 1
while len(data) > 1:
    print_matrix2(data, i)
    print('\n')
    step(data)
    i += 1
print('\n')
print_matrix2(data, i)
print('\n')
