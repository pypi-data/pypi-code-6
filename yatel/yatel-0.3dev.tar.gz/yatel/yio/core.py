#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


# =============================================================================
# DOC
# =============================================================================

"""Base structure for Yatel parsers."""


# =============================================================================
# IMPORTS
# =============================================================================

try:
    import cStringIO as StringIO
except:
    import StringIO

import abc


# =============================================================================
# CONSTANTS
# =============================================================================

#: Parser version number (tuple).
YF_VERSION = ("0", "5")
#: Parser version number (string).
YF_STR_VERSION = ".".join(YF_VERSION)


# =============================================================================
# CLASS
# =============================================================================

class BaseParser(object):
    """Base class for parsers."""

    __metaclass__ = abc.ABCMeta

    @classmethod
    def version(cls):
        """Returns version of parser."""
        return YF_STR_VERSION

    @classmethod
    def file_exts(cls):
        raise NotImplementedError()

    def dumps(self, nw, *args, **kwargs):
        """Serializes a yatel db to a formatted string.

        Parameters
        ----------
        nw : :py:class:`yatel.db.YatelNetwork`
            Network source of data.
        
        Returns
        -------
        string : str
            Json formatted string.
        
        """
        fp = StringIO.StringIO()
        self.dump(nw, fp, *args, **kwargs)
        return fp.getvalue()

    def loads(self, nw, string, *args, **kwargs):
        """Deserializes a formatted string to add it into the yatel database.
        
        Parameters
        ----------
        nw : :py:class:`yatel.db.YatelNetwork`
            Network destination for data.
        string : str
            String to be deserialize.
        
        """
        fp = StringIO.StringIO(string)
        self.load(nw, fp, *args, **kwargs)

    @abc.abstractmethod
    def dump(self, nw, fp, *args, **kwargs):
        """**Abstract Method.**
        
        Serializes data from a yatel network to a file.
        
        Raises
        ------
            NotImplementedError
        
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def load(self, nw, fp, *args, **kwargs):
        """**Abstract Method.**
        
        Deserializes data from a file and adds it to the yatel network.
        
        Raises
        ------
            NotImplementedError
        
        """
        raise NotImplementedError()

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print(__doc__)
