#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#==============================================================================
# DOCS
#==============================================================================

"""Levnshtetin and Damerau Levenshteing distance implementation of yatel.

- http://en.wikipedia.org/wiki/Levenshtein_distance
- http://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance


"""

#==============================================================================
# IMPORTS
#==============================================================================

from yatel.weight import core


#==============================================================================
# LEVENSHTEIN
#==============================================================================

class Levenshtein(core.BaseWeight):
    """The Levenshtein distance between two haplotypes is defined as the
    minimum number of edits needed to transform one haplotype as squence
    (sumatory of attribute values) into the other, with the  allowable edit
    operations being insertion, deletion, or substitution of a single character

    Note: Previously the haplotypes attribute values are encoded with to_seq
          funcion.

    """

    @classmethod
    def names(cls):
        return "levenshtein", "lev"

    def __init__(self, to_seq=None):
        """Creates a new instance
        
        Parameters
        ----------
        to_seq : callable
            a callable for convert any object to a string. By defautl see 
            yatel.weight.levenshtein.to_seq_default

        """
        self.to_seq = to_seq_default if to_seq is None else to_seq

    def weight(self, hap0, hap1):
        """A ``float`` distance between 2 `dom.Haplotype` instances"""

        def levenshtein(a, b):
            """Calculates the Levenshtein distance between a and b.

            Found at: http://hetland.org/coding/
            """
            n, m = len(a), len(b)
            if n > m:
                # Make sure n <= m, to use O(min(n,m)) space
                a, b = b, a
                n, m = m, n
            current = range(n + 1)
            for i in range(1, m + 1):
                previous, current = current, [i] + [0] * n
                for j in range(1, n + 1):
                    add, delete = previous[j] + 1, current[j - 1] + 1
                    change = previous[j - 1]
                    if a[j - 1] != b[i - 1]:
                        change = change + 1
                    current[j] = min(add, delete, change)
            return current[n]

        value = 0
        for name in sorted(set(hap0.keys() + hap1.keys())):
            as0 = self.to_seq(hap0.get(name))
            as1 = self.to_seq(hap1.get(name))
            value += levenshtein(as0, as1)
        return value


#==============================================================================
# DAMERAU-LEVENSHTEIN
#==============================================================================

class DamerauLevenshtein(Levenshtein):
    """Calculate the Damerau-Levenshtein distance between haplotypes.

    This distance is the number of additions, deletions, substitutions,
    and transpositions needed to transform the first haplotypes as sequences
    into the second.

    Transpositions are exchanges of *consecutive* characters; all other
    operations are self-explanatory.

    This implementation is O(N*M) time and O(M) space, for N and M the
    lengths of the two sequences.

    Note: Previously the haplotypes attribute values are *base64* endoced

    """

    @classmethod
    def names(cls):
        return "dameraulevenshtein", "damlev", "damerau-levenshtein"

    def weight(self, hap0, hap1):
        """A ``float`` distance between 2 `dom.Haplotype` instances"""

        def dameraulevenshtein(seq1, seq2):
            """This is the original code found in:

            http://mwh.geek.nz/2009/04/26/python-damerau-levenshtein-distance/

            The code is available under the MIT licence, in the hope that it
            will be useful, but without warranty of any kind. I have also
            included a codesnippet  GUID in line with the linked post, as a
            sort of experiment. Please leave that comment intact if you’re
            posting a derivative somewhere, and add your own.

            """
            # codesnippet:D0DE4716-B6E6-4161-9219-2903BF8F547F
            # Conceptually, this is based on a len(seq1) + 1 * len(seq2) + 1
            # matrix.
            # However, only the current and two previous rows are needed at
            # once, so we only store those.
            oneago = None
            thisrow = range(1, len(seq2) + 1) + [0]
            for x in xrange(len(seq1)):
                # Python lists wrap around for negative indices, so put the
                # leftmost column at the *end* of the list. This matches with
                # the zero-indexed strings and saves extra calculation.
                twoago, oneago, thisrow = (
                    oneago, thisrow, [0] * len(seq2) + [x + 1]
                )
                for y in xrange(len(seq2)):
                    delcost = oneago[y] + 1
                    addcost = thisrow[y - 1] + 1
                    subcost = oneago[y - 1] + (seq1[x] != seq2[y])
                    thisrow[y] = min(delcost, addcost, subcost)
                    # This block deals with transpositions
                    if (
                        x > 0 and y > 0 and seq1[x] == seq2[y - 1]
                        and seq1[x - 1] == seq2[y] and seq1[x] != seq2[y]
                    ):
                        thisrow[y] = min(thisrow[y], twoago[y - 2] + 1)
            return thisrow[len(seq2) - 1]

        value = 0
        for name in sorted(set(hap0.keys() + hap1.keys())):
            as0 = self.to_seq(hap0.get(name))
            as1 = self.to_seq(hap1.get(name))
            value += dameraulevenshtein(as0, as1)
        return value


#==============================================================================
# FUNCTIONS
#==============================================================================

def to_seq_default(obj):
    """Convert a given object to a normalized as base64 of self

    """
    if obj is None:
        return ""
    else:
        text = obj if isinstance(obj, unicode) else unicode(obj)
        return text.encode("base64")


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
