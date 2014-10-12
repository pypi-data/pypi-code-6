# VERSION
from . import mimodd_base
version = mimodd_base.Version((0, 0, 2))

import random

class Chromosome (object):
    """An object representation of a chromosome.

    Uses 1-based coordinates."""
    
    def __init__ (self, name, length):
        self.name= name
        self.length= length

    def randpos (self, start=1, end=None, relpos=False):
        """Returns a random nucleotide position from the chromosome.

        start and end specify an inclusive interval."""

        if end is None:
            end = self.length
        if relpos:
            end = self.length-end
        if not 1 <= start <= self.length:
            raise ValueError ('start position outside chromosome boundaries.')
        if not start <= end <= self.length:
            raise ValueError ('invalid end position (smaller than start or outside chromosome boundaries.')
        return random.randrange(start, end+1)

class Deletion (object):
    def __init__(self, chrm, start, stop, sample = None):
        self.chromosome = chrm
        self.start = start
        self.stop = stop
