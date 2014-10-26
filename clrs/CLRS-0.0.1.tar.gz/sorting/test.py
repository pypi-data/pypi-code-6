import unittest
import random
from sorting import *


class Sorting(unittest.TestCase):
    def setUp(self):
        self.array = list(range(100))
        self.array_clone = self.array[:]
        random.shuffle(self.array)

    def test_insertion_sort(self):
        insertion_sort(self.array)
        self.assertEqual(self.array, self.array_clone)

    def test_selection_sort(self):
        selection_sort(self.array)
        self.assertEqual(self.array, self.array_clone)

    def test_bubble_sort(self):
        bubble_sort(self.array)
        self.assertEqual(self.array, self.array_clone)

    def test_merge_sort(self):
        merge_sort(self.array)
        self.assertEqual(self.array, self.array_clone)

    # def test_bucket_sort(self):
    # bucket_sort(self.array)
    #     self.assertEqual(self.array, self.array_clone)

    def test_counting_sort(self):
        counting_sort(self.array, len(self.array) + 3)
        self.assertEqual(self.array, self.array_clone)

    def test_heap_sort(self):
        heap_sort(self.array)
        self.assertEqual(self.array, self.array_clone)

    def test_quick_sort(self):
        quick_sort(self.array)
        self.assertEqual(self.array, self.array_clone)

    def test_radix_sort(self):
        radix_sort(self.array, 2)
        self.assertEqual(self.array, self.array_clone)


if __name__ == '__main__':
    unittest.main()