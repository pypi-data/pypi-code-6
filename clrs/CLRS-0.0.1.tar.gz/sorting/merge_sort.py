def merge_sort(array):
    def merge(array, low, middle, high):
        left = array[low:middle + 1]
        left.append(float('inf'))
        right = array[middle + 1:high + 1]
        right.append(float('inf'))

        p_left = 0
        p_right = 0
        for i in range(low, high + 1):
            if left[p_left] < right[p_right]:
                array[i] = left[p_left]
                p_left += 1
            else:
                array[i] = right[p_right]
                p_right += 1

    def merge_sort_inner(array, low, high):
        if low >= high:
            return
        middle = (low + high) // 2
        merge_sort_inner(array, low, middle)
        merge_sort_inner(array, middle + 1, high)
        merge(array, low, middle, high)

    merge_sort_inner(array, 0, len(array) - 1)