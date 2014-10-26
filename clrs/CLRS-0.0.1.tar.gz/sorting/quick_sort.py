def quick_sort(array):
    def quick_sort_inner(array, low, high):
        if low >= high:
            return
        middle = low
        for i in range(low + 1, high + 1):
            if array[i] < array[middle]:
                array[middle], array[i], array[middle + 1] = array[i], array[middle + 1], array[middle]
                middle += 1

        quick_sort_inner(array, low, middle - 1)
        quick_sort_inner(array, middle + 1, high)

    quick_sort_inner(array, 0, len(array) - 1)