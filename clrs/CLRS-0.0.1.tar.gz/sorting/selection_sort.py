def selection_sort(array):
    for i in range(len(array) - 1, 0, -1):
        max_element_index = 0
        for j in range(0, i + 1):
            if array[max_element_index] < array[j]:
                max_element_index = j

        array[max_element_index], array[i] = array[i], array[max_element_index]