import solution, solution_src

import random, json
import pytest

def test_solution():
    items_count = 100
    unsorted_ar = [random.randint(0, 1000) for n in range(items_count)]
    sorted_ar = sorted(unsorted_ar)
    for item in unsorted_ar:
        assert solution.search(sorted_ar, item) == sorted_ar.index(item)

def test_solution_src():
    assert None == solution_src.search(None, None)
