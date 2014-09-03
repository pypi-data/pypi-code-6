__all__ = ('capabilities',)

VERSION = (0, 1, 0)
__version__ = '.'.join(map(str, VERSION))

AUTHORS = (
    'Ian A Wilson',
)
__author__ = ', '.join(AUTHORS)


from .structure import capabilities  # noqa
