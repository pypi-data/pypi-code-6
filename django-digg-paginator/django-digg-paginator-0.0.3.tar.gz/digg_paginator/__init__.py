__version__ = '0.0.4'
VERSION = tuple(map(int, __version__.split('.')))

from .paginators import ExPaginator, DiggPaginator, QuerySetDiggPaginator
