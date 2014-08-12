from __future__ import absolute_import, division, print_function

from .__about__ import (
    __author__, __copyright__, __email__, __license__, __summary__, __title__,
    __uri__, __version__
)

__all__ = [
    "__title__", "__summary__", "__uri__", "__version__", "__author__",
    "__email__", "__license__", "__copyright__", "binary_search"
]

def binary_search(data, target, lo=0, hi=None):
    """
    Perform binary search on sorted list data for target. Returns int
    representing position of target in data.
    """
    hi = hi if hi is not None else len(data)
    mid = (lo + hi) // 2
    if data[mid] > target:
        return binary_search(data, target, lo=lo, hi=mid)
    elif data[mid] < target:
        return binary_search(data, target, lo=(mid + 1), hi=hi)
    elif data[mid] == target:
        return mid
    elif hi < 0:
        return -1
