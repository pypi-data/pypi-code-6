VERSION = (0, 1, 0)
AUTHOR = (
    'Ian A Wilson',
)

# need to convert tuple of ints to tuple of strings
__version__ = '.'.join(map(str, VERSION))
__author__ = ', '.join(AUTHOR)
