#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


#===============================================================================
# DOC
#===============================================================================

"""Persists Yatel databases in json format.

"""


#===============================================================================
# IMPORTS
#===============================================================================

import json

from yatel import typeconv
from yatel.yio import core


#===============================================================================
# CLASS
#===============================================================================

class JSONParser(core.BaseParser):
    """JSON parser to serialize and deserialize data."""

    @classmethod
    def file_exts(cls):
        """Returns extensions used for JSON handling."""
        return ("yjf", "json")

    def dump(self, nw, fp, *args, **kwargs):
        """Serializes data from a Yatel network to a JSON file-like stream.
        
        Parameters
        ----------
        nw : :py:class:`yatel.db.YatelNetwork`
            Network source of data.
        fp : file-like object
            Target  for serialization.

        """
        kwargs["ensure_ascii"] = kwargs.get("ensure_ascii", True)
        data = {
            "haplotypes":  map(typeconv.simplifier, nw.haplotypes()),
            "facts": map(typeconv.simplifier, nw.facts()),
            "edges": map(typeconv.simplifier, nw.edges()),
            "version": self.version(),
        }
        json.dump(data, fp, *args, **kwargs)

    def load(self, nw, fp, *args, **kwargs):
        """Deserializes data from a JSON file-like stream and adds it to the 
        yatel network.
        
        Parameters
        ----------
        nw : :py:class:`yatel.db.YatelNetwork`
            Network target of data.
        fp : file-like object
            Source of data to deserialize.
        
        """
        data = json.load(fp, *args, **kwargs)
        nw.add_elements(map(typeconv.parse, data["haplotypes"]))
        nw.add_elements(map(typeconv.parse, data["facts"]))
        nw.add_elements(map(typeconv.parse, data["edges"]))


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
