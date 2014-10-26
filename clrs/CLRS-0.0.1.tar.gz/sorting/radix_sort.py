def radix_sort(array, d):
    """All element of array should have less then d bits"""
    for i in range(d):
        array.sort(key=(lambda integer: integer // pow(10, i) % 10))