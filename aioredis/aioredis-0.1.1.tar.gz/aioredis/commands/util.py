from collections import namedtuple


_ScanResult = namedtuple('_ScanResult', 'cursor items')


class _ScanContext(_ScanResult):
    __slots__ = ()

    def __iter__(self):
        pass
