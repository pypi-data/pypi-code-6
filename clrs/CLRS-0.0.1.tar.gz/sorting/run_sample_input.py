import random
import math
import string
import time

from sorting import *


def sample_int_array(n):
    input = []
    for i in range(n):
        input.append(random.randint(1, 65535))
    return input


def sample_string_array(n):
    input = []
    for i in range(n):
        s = ''.join(random.sample(string.ascii_lowercase, 16))
        input.append(s)
    return input


def run_a_test(input, sort_method, *args):
    input_clone = input[:]
    start = time.time()
    if args:
        sort_method(input_clone, args[0])
    else:
        sort_method(input_clone)
    end = time.time() - start
    # print(input_clone[:5])
    print('{sort_method.__name__:20}{time:.3f}'.format(sort_method=sort_method, time=math.log2(end)))


if __name__ == '__main__':
    input = sample_int_array(2 ** 12)
    # print(input)
    print('sample produced')
    run_a_test(input, insertion_sort)
    run_a_test(input, quick_sort)
    run_a_test(input, merge_sort)
    run_a_test(input, radix_sort, 5)
    run_a_test(input, counting_sort, 65536)
    run_a_test(input, heap_sort)