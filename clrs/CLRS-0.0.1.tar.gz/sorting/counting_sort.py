def counting_sort(array, k):
    """All element of array should be in range [0,k)"""
    array_clone = array[:]
    count_array = [0] * k
    for e in array_clone:
        count_array[e] += 1
    for i in range(1, k):
        count_array[i] += count_array[i - 1]

    for i in range(len(array_clone) - 1, -1, -1):
        array[count_array[array_clone[i]] - 1] = array_clone[i]
        count_array[array_clone[i]] -= 1