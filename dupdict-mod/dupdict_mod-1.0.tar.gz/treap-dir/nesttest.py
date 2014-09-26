#!/usr/bin/python3

import sys

import nest
import random


def shuffle(list_):
    len_list = len(list_)
    for index in range(len_list):
        index2 = int(random.random() * len_list)
        list_[index], list_[index2] = list_[index2], list_[index]
    

def m_lowest_of_n_unique(m, n):
    #print('computing the {} lowest values in a list of {} unique values in random order'.format(m, n))
    keep = nest.nlowest(m)
    list_ = list(range(n))
    shuffle(list_)
    for value in list_:
        keep.add(value)
    actual_result = list(keep)
    expected_result = list(range(m))
    if actual_result == expected_result:
        return True
    else:
        sys.stderr.write('{}: m_lowest_of_n_unique: test failed\n'.format(sys.argv[0]))
        sys.stderr.write('actual_result  : {}\n'.format(actual_result))
        sys.stderr.write('expected_result: {}\n'.format(expected_result))
        return False


def m_highest_of_n_unique(m, n):
    #print('computing the {} highest values in a list of {} unique values in random order'.format(m, n))
    keep = nest.nhighest(m)
    list_ = list(range(n))
    shuffle(list_)
    for value in list_:
        keep.add(value)
    actual_result = list(keep)
    expected_result = list(range(n - 1, n - m - 1, -1))
    if actual_result == expected_result:
        return True
    else:
        sys.stderr.write('{}: m_highest_of_n_unique: test failed\n'.format(sys.argv[0]))
        sys.stderr.write('actual_result  : {}\n'.format(actual_result))
        sys.stderr.write('expected_result: {}\n'.format(expected_result))
        return False
        

def expensive_but_simple_duplicate_result_lowest(list_, m):
    list2 = list_[:]
    list2.sort()
    return list2[:m]


def expensive_but_simple_duplicate_result_highest(list_, m):
    list2 = list_[:]
    list2.sort()
    return list(reversed(list2[-m:]))


def m_lowest_of_n_duplicate(m, n):
    #print('computing the {} lowest values in a list of {} duplicate values in random order'.format(m, n))
    keep = nest.nlowest(m, allow_duplicates=True)
    list_ = list(range(n // 2)) + list(range(n // 2))
    shuffle(list_)
    for value in list_:
        keep.add(value)
    actual_result = list(keep)
    expected_result = expensive_but_simple_duplicate_result_lowest(list_, m)
    if actual_result == expected_result:
        return True
    else:
        sys.stderr.write('{}: m_lowest_of_n_duplicate: test failed\n'.format(sys.argv[0]))
        sys.stderr.write('actual_result  : {}\n'.format(actual_result))
        sys.stderr.write('expected_result: {}\n'.format(expected_result))
        return False


def m_highest_of_n_duplicate(m, n):
    #print('computing the {} highest values in a list of {} duplicate values in random order'.format(m, n))
    keep = nest.nhighest(m, allow_duplicates=True)
    list_ = list(range(n // 2)) + list(range(n // 2))
    shuffle(list_)
    for value in list_:
        keep.add(value)
    actual_result = list(keep)
    expected_result = expensive_but_simple_duplicate_result_highest(list_, m)
    if actual_result == expected_result:
        return True
    else:
        sys.stderr.write('{}: m_highest_of_n_duplicate: test failed\n'.format(sys.argv[0]))
        sys.stderr.write('actual_result  : {}\n'.format(actual_result))
        sys.stderr.write('expected_result: {}\n'.format(expected_result))
        return False
        

def main():
    all_good = True

    m = 3
    n = 10

    all_good &= m_lowest_of_n_unique(m, n)
    all_good &= m_highest_of_n_unique(m, n)
    all_good &= m_lowest_of_n_duplicate(m, n)
    all_good &= m_highest_of_n_duplicate(m, n)

    if all_good:
        sys.exit(0)
    else:
        sys.stderr.write('{}: One or more tests failed\n'.format(sys.argv[0]))
        sys.exit(1)


main()

