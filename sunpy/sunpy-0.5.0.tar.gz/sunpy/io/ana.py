"""
ANA File Reader

.. warning::
    This code currently has an unresolved bug under Windows, it may not work as expected.

Notes
-----
ANA is a script that allows people to access compressed ana files.
It accesses a C library, based on Michiel van Noort's
IDL DLM library 'f0' which contains a cleaned up version of the original
anarw routines.

Created by Tim van Werkhoven (t.i.m.vanwerkhoven@gmail.com) on 2009-02-11.
Copyright (c) 2009--2011 Tim van Werkhoven.
"""
 
from __future__ import absolute_import
import os

try:
    from sunpy.io import _pyana
except ImportError: # pragma: no cover
    _pyana = None # pragma: no cover

from sunpy.io.header import FileHeader

__all__ = ['read', 'get_header', 'write']

def read(filename, debug=False):
    """
    Loads an ANA file and returns the data and a header in a list of (data,
    header) tuples.
    
    Parameters
    ----------
    filename: string
        Name of file to be read.
    debug: bool, optional
        Prints versbose debug information.
    
    Returns
    -------
    out: list
        A list of (data, header) tuples
    
    Examples
    --------
    >>> data = sunpy.io.ana.read(filename)
    
    """
    if not os.path.isfile(filename):
        raise IOError("File does not exist!")

    if _pyana is None:
        raise ImportError("C extension for ANA is missing, please rebuild") # pragma: no cover

    data = _pyana.fzread(filename, debug)
    return [(data['data'],FileHeader(data['header']))]

def get_header(filename, debug=False):
    """
    Loads an ANA file and only return the header consisting of the dimensions,
    size (defined as the product of all dimensions times the size of the
    datatype, this not relying on actual filesize) and comments.

    Parameters
    ----------
    filename: string
        Name of file to be read.
    debug: bool, optional
        Prints versbose debug information.
    
    Returns
    -------
    out: list
        A list of FileHeader headers

    Examples
    --------    
    >>> header = sunpy.io.ana.get_header(filename)
    """
    if _pyana is None:
        raise ImportError("C extension for ANA is missing, please rebuild")# pragma: no cover

    data = _pyana.fzread(filename, debug)
    return [FileHeader(data['header'])]

def write(filename, data, comments=False, compress=1, debug=False):
    """
    Saves a 2D numpy array as an ANA file and returns the bytes written or NULL

    Parameters
    ----------
    filename: string
        Name of file to be created.
    data: numpy array
        Name of data to be stored.
    comments: FileHeader, optional
        The comments to be stored as a header.
    compress: int, optional
        To compress the data or not.
        1 is to compress, 0 is uncompressed
    debug: bool, optional
        Prints versbose debug information.
    
    Returns
    -------
    out: ANA compressed archive
        A new ANA compressed archive containing the data and header.    

    Examples
    --------    
    >>> written = sunpy.io.ana.write(filename, data, comments=Falsem, compress=1)
    """
    if _pyana is None:
        raise ImportError("C extension for ANA is missing, please rebuild")# pragma: no cover

    if comments:
        return _pyana.fzwrite(filename, data, compress, comments, debug)
    else:
        return _pyana.fzwrite(filename, data, compress, '', debug)
