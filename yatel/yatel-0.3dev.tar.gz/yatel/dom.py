#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


#===============================================================================
# DOCS
#===============================================================================

"""Domain Object Model for Yatel.

"""

#===============================================================================
# IMPORTS
#===============================================================================

import collections


#===============================================================================
# BASE CLASS
#===============================================================================

class YatelDOM(collections.Mapping):
    """Base class for yatel objects, handling arbitrary keys.
    
    """

    CLEAN_NULL = True

    def __init__(self, **attrs):
        if "id" in attrs:
            raise ValueError("'id' is not valid attribute name")
        self._data = dict([
            [k, v] for k, v in attrs.items() if v is not None
        ]) if self.CLEAN_NULL else attrs
        super(YatelDOM, self).__init__()

    def __getitem__(self, k):
        """x.__getitem__(k) <==> x[k]"""
        return self._data[k]

    def __iter__(self):
        """x.__iter__() <==> iter(x)"""
        return iter(self._data)

    def __len__(self):
        """x.__len__() <==> len(x)"""
        return len(self._data)

    def __eq__(self, obj):
        """x.__eq__(y) <==> x==y"""
        return isinstance(obj, type(self)) and self._data == obj._data

    def __hash__(self):
        """x.__hash__() <==> hash(x)"""
        return hash(tuple(self._data.items()))

    def __ne__(self, obj):
        """x.__ne__(y) <==> x!=y"""
        return not (self == obj)

    def __getattr__(self, n):
        """x.__getattr__('name') <==> x.name <==> x['name']"""
        try:
            return self._data[n]
        except KeyError:
            t = type(self).__name__
            msg = "'{t}' object has no attribute '{n}'".format(t=t, n=n)
            raise AttributeError(msg)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        return repr(self._data)


#===============================================================================
# HAPLOTYPES
#===============================================================================

class Haplotype(YatelDOM):
    """Represents an individual class or group with similar characteristics
    to be analized."""

    def __init__(self, hap_id, **attrs):
        """Creates a new instance

        Parameters
        ----------
            hap_id : Unique id of this haplotype.
            attrs : Different attributes of this haplotype.

        """
        if hap_id is None:
            raise ValueError("'hap_id' can't be None")
        attrs["hap_id"] = hap_id
        super(Haplotype, self).__init__(**attrs)


    def __eq__(self, obj):
        """x.__eq__(y) <==> x==y"""
        return isinstance(obj, Haplotype) and self.hap_id == obj.hap_id

    def __hash__(self):
        """x.__hash__() <==> hash(x)"""
        return hash(self.hap_id)

    def __ne__(self, obj):
        """x.__ne__(y) <==> x!=y"""
        return not (self == obj)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        cls = type(self).__name__
        desc = self.hap_id
        at = hex(id(self))
        return "<{cls} ({desc}) at {at}>".format(cls=cls, desc=desc, at=at)


#===============================================================================
# FACT
#===============================================================================

class Fact(YatelDOM):
    """Fact represents a *metadata* of the `haplotype`.

    For example if you gather in two places the same `haplotype`,
    the characteristics of these places correspond to different *facts* of the
    same `haplotype`.

    """

    def __init__(self, hap_id, **attrs):
        """Creates a new instance

        Parameters
        ----------
        hap_id : The `dom.Haplotype` id of this `fact`.
        attrs : Different attributes of this `fact`.

        """
        if hap_id is None:
            raise ValueError("'hap_id' can't be None")
        attrs["hap_id"] = hap_id
        super(Fact, self).__init__(**attrs)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        cls = type(self).__name__
        desc = "of Haplotype '{hap_id}'".format(hap_id=self.hap_id)
        at = hex(id(self))
        return "<{cls} ({desc}) at {at}>".format(cls=cls, desc=desc, at=at)


#===============================================================================
# Edge
#===============================================================================

class Edge(YatelDOM):
    """Represents a relation between 2 or more `haplotypes`.

    """
    CLEAN_NULL = False

    def __init__(self, weight, haps_id):
        """Creates a new instance.

        Parameters
        ----------
        weight : The degree of relationship between `haplotypes`.
        haps_id : The list of the related `haplotypes`.

        """
        super(Edge, self).__init__(
            weight=float(weight), haps_id=tuple(haps_id)
        )

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        cls = type(self).__name__
        desc = "{weight} {haps_id}".format(
            weight=self.weight, haps_id=str(self.haps_id)
        )
        at = hex(id(self))
        return "<{cls} ({desc}) at {at}>".format(cls=cls, desc=desc, at=at)


#===============================================================================
# ENVIROMENT
#===============================================================================

class Environment(YatelDOM):
    """Represents an iterable dictionary of dictionaries with valid 
    combinations of values of the attributes given when the instance is created.
    
    """
    CLEAN_NULL = False

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        cls = type(self).__name__
        desc = super(Environment, self).__repr__()
        at = hex(id(self))
        return "<{cls} {desc} at {at}>".format(cls=cls, desc=desc, at=at)


#===============================================================================
# DESCRIPTOR
#===============================================================================

class Descriptor(YatelDOM):
    """Represents detailed information of a network.

    """

    CLEAN_NULL = False

    def __init__(self, mode, fact_attributes,
                 haplotype_attributes, edge_attributes, size):
        """Creates a new instance.

        Parameters
        ----------
        edges_attributes : dict
            Dictionary contains always 2 keys: `max_nodes` How many nodes 
            connect the edge with maximun number of connections. And `weight` 
            the time od weight attribute
        fact_attributes : dict
            Contains an arbitrary number of keys, with keys as attributes 
            name, and value as attribute type.
        haplotype_atributes : dict
            Contains an arbitrary number of keys, with keys as attributes 
            name, and value as attribute type.
        mode : str
            Actual mode of the network
        size : dict
            Has the number of elements in the network discrimined by type 
            haplotypes, facts and edges.
            
        """
        super(Descriptor, self).__init__(
            mode=mode, fact_attributes=fact_attributes,
            haplotype_attributes=haplotype_attributes,
            edge_attributes=edge_attributes, size=size
        )

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        cls = type(self).__name__
        desc = super(Descriptor, self).__repr__()
        at = hex(id(self))
        return "<{cls} '{desc}' at {at}>".format(cls=cls, desc=desc, at=at)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




