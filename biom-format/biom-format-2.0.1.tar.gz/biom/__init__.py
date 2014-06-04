#!/usr/bin/env python
r"""
Quick start
===========

.. currentmodule:: biom

BIOM has an example table and two methods for reading in `Table` objects that
are immediately available at the package level.

Functions
---------

.. autosummary::
   :toctree: generated/

   load_table

Examples
--------
Load an example table:

>>> from biom import example_table
>>> print example_table # doctest: +NORMALIZE_WHITESPACE
# Constructed from biom file
#OTU ID S1  S2  S3
O1  0.0 1.0 2.0
O2  3.0 4.0 5.0

Parse a table from an open file object:

>>> from biom import parse_table
>>> with open('path/to/table.biom') as f: # doctest: +SKIP
...     table = parse_table(f)

Parse a table from a path. BIOM will attempt to determine if the fhe file is
either in TSV, HDF5, JSON, gzip'd JSON or gzip'd TSV and parse accordingly:

>>> from biom import load_table
>>> table = load_table('path/to/table.biom') # doctest: +SKIP

"""
# ----------------------------------------------------------------------------
# Copyright (c) 2011-2013, The BIOM Format Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2011-2013, The BIOM Format Development Team"
__credits__ = ["Daniel McDonald", "Jai Ram Rideout", "Greg Caporaso",
               "Jose Clemente", "Justin Kuczynski", "Antonio Gonzalez",
               "Yoshiki Vazquez Baeza", "Jose Navas", "Adam Robbins-Pianka",
               "Rob Knight", "Joshua Shorenstein", "Emily TerAvest"]
__license__ = "BSD"
__url__ = "http://biom-format.org"
__version__ = "2.0.1"
__maintainer__ = "Daniel McDonald"
__email__ = "daniel.mcdonald@colorado.edu"


from .table import Table
from .parse import parse_biom_table as parse_table

example_table = Table([[0, 1, 2], [3, 4, 5]], ['O1', 'O2'],
                      ['S1', 'S2', 'S3'],
                      [{'taxonomy': ['Bacteria', 'Firmicutes']},
                       {'taxonomy': ['Bacteria', 'Bacteroidetes']}],
                      [{'environment': 'A'},
                       {'environment': 'B'},
                       {'environment': 'A'}], input_is_dense=True)


def load_table(f):
    r"""Load a `Table` from a path

    Parameters
    ----------
    f : str

    Returns
    -------
    Table

    Raises
    ------
    IOError
        If the path does not exist
    TypeError
        If the data in the path does not appear to be a BIOM table

    Examples
    --------
    Parse a table from a path. BIOM will attempt to determine if the fhe file
    is either in TSV, HDF5, JSON, gzip'd JSON or gzip'd TSV and parse
    accordingly:

    >>> from biom import load_table
    >>> table = load_table('path/to/table.biom') # doctest: +SKIP

    """
    from biom.util import biom_open
    with biom_open(f) as fp:
        try:
            table = parse_table(fp)
        except (IndexError, TypeError):
            raise TypeError("%s does not appear to be a BIOM file!" % f)
    return table


__all__ = ['Table', 'example_table', 'parse_table', 'load_table']
