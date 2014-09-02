#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 'THE WISKEY-WARE LICENSE':
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Persists Yatel databases in XML format.

"""

#===============================================================================
# IMPORTS
#===============================================================================

from xml import sax
from xml.sax import saxutils

from yatel import typeconv
from yatel.yio import core


#===============================================================================
# IO FUNCTIONS
#===============================================================================

class XMLParser(core.BaseParser):
    """XML parser to serialize and deserialize data."""

    @classmethod
    def file_exts(cls):
        """Returns extensions used for XML handling."""
        return ("yxf", "xml")

    #===========================================================================
    # DUMP
    #===========================================================================

    def start_elem(self, tag, attrs={}):
        attrs = u' '.join([u'{}={}'.format(k, saxutils.quoteattr(v))
                                           for k, v in attrs.items()])
        return u'<{tag} {attrs}>'.format(tag=tag, attrs=attrs)

    def end_elem(self, tag):
        return u'</{tag}>'.format(tag=tag)

    def to_content(self, data):
        return saxutils.escape(str(data))


    def dump(self, nw, fp, *args, **kwargs):
        """Serializes data from a Yatel network to a XML file-like stream.
        
        Parameters
        ----------
        nw : :py:class:`yatel.db.YatelNetwork`
            Network source of data.
        fp : file-like object
            Target for serialization.
        
        """

        fp.write(self.start_elem(u"Network", {u"version": self.version()}))

        fp.write(self.start_elem(u"Haplotypes"))
        for hap in nw.haplotypes():
            fp.write(self.start_elem(u"Haplotype"))
            for aname, adata in typeconv.simplifier(hap)["value"].items():
                xmlattrs = {u"name": aname, u"type": adata["type"]}
                fp.write(self.start_elem(u"Attribute", xmlattrs))
                fp.write(self.to_content(adata["value"]))
                fp.write(self.end_elem(u"Attribute"))
            fp.write(self.end_elem(u"Haplotype"))
        fp.write(self.end_elem(u"Haplotypes"))

        fp.write(self.start_elem(u"Facts"))
        for fact in nw.facts():
            fp.write(self.start_elem(u"Fact"))
            for aname, adata in typeconv.simplifier(fact)["value"].items():
                xmlattrs = {u"name": aname, u"type": adata["type"]}
                fp.write(self.start_elem(u"Attribute", xmlattrs))
                fp.write(self.to_content(adata["value"]))
                fp.write(self.end_elem(u"Attribute"))
            fp.write(self.end_elem(u"Fact"))
        fp.write(self.end_elem(u"Facts"))

        fp.write(self.start_elem(u"Edges"))
        for edge in nw.edges():
            fp.write(self.start_elem(u"Edge"))
            attrs = typeconv.simplifier(edge)["value"]

            xmlattrs = {u"name": "weight", u"type": attrs["weight"]["type"]}
            fp.write(self.start_elem(u"Attribute", xmlattrs))
            fp.write(self.to_content(attrs["weight"]["value"]))
            fp.write(self.end_elem(u"Attribute"))

            fp.write(self.start_elem(u"Attribute",
                {u"name": u"haps_id", u"type": attrs["haps_id"]["type"]}
            ))
            for hap_id_data in attrs["haps_id"]["value"]:
                xmlattrs = {"name": u"hap_id", u"type": hap_id_data["type"]}
                fp.write(self.start_elem(u"Attribute", xmlattrs))
                fp.write(self.to_content(hap_id_data["value"]))
                fp.write(self.end_elem(u"Attribute"))
            fp.write(self.end_elem(u"Attribute"))
            fp.write(self.end_elem(u"Edge"))
        fp.write(self.end_elem(u"Edges"))


        fp.write(self.end_elem(u"Network"))


    #===========================================================================
    # LOAD
    #===========================================================================

    def load(self, nw, fp, *args, **kwargs):
        """Deserializes data from a XML file-like stream and adds it to the 
        Yatel network.
        
        Parameters
        ----------
        nw : :py:class:`yatel.db.YatelNetwork`
            Network target of data.
        fp : file-like object
            Source of data to deserialize.
        
        """

        class YatelXMLHandler(sax.ContentHandler):

            def __init__(self, parent, *args, **kwargs):

                self.version = None

                self.stk = []
                self.buff = None
                self.parent = parent

            def startElement(self, name, attrs):
                self.stk.append(name.title())

                # first element
                if self.stk == ["Network"]:
                    self.version = saxutils.unescape(attrs[u"version"])

                # haplotypes
                elif self.stk == ["Network", "Haplotypes", "Haplotype"]:
                    self.buff = {"last": None, "attrs": {}}
                elif self.stk == ["Network", "Haplotypes", "Haplotype", "Attribute"]:
                    aname = saxutils.unescape(attrs["name"])
                    atype = saxutils.unescape(attrs["type"])
                    self.buff["last"] =  {"name": aname, "type": atype}

                # facts
                elif self.stk == ["Network", "Facts", "Fact"]:
                    self.buff = {"last": None, "attrs": {}}
                elif self.stk == ["Network", "Facts", "Fact", "Attribute"]:
                    aname = saxutils.unescape(attrs["name"])
                    atype = saxutils.unescape(attrs["type"])
                    self.buff["last"] =  {"name": aname, "type": atype}

                # edges
                elif self.stk == ["Network", "Edges", "Edge"]:
                    self.buff = {"weight": None, "haps_id": None}
                elif self.stk == ["Network", "Edges", "Edge", "Attribute"]:
                    aname = saxutils.unescape(attrs["name"])
                    atype = saxutils.unescape(attrs["type"])
                    if aname == "weight":
                        self.buff["weight"] = {"type": atype}
                    if aname == "haps_id":
                        self.buff["haps_id"] = {"type": atype, "value": []}
                elif self.stk == ["Network", "Edges", "Edge", "Attribute", "Attribute"]:
                    atype = saxutils.unescape(attrs["type"])
                    self.buff["haps_id"]["value"].append({"type": atype})

            def characters(self, content):
                content = saxutils.unescape(content)

                # haplotypes
                if self.stk == ["Network", "Haplotypes", "Haplotype", "Attribute"]:
                    aname = self.buff["last"]["name"]
                    atype = self.buff["last"]["type"]
                    self.buff["attrs"][aname] = {
                        u"type": atype, u"value": content
                    }

                # facts
                elif self.stk == ["Network", "Facts", "Fact", "Attribute"]:
                    aname = self.buff["last"]["name"]
                    atype = self.buff["last"]["type"]
                    self.buff["attrs"][aname] = {
                        u"type": atype, u"value": content
                    }

                # edges
                elif self.stk == ["Network", "Edges", "Edge", "Attribute"]:
                    self.buff["weight"]["value"] = content
                elif self.stk == ["Network", "Edges", "Edge", "Attribute", "Attribute"]:
                    self.buff["haps_id"]["value"][-1]["value"] = content

            def endElement(self, name):
                if self.stk[-1] != name.title():
                    return

                # haplotypes
                elif self.stk == ["Network", "Haplotypes", "Haplotype"]:
                    data = {
                        u"type": "Haplotype",
                        u"value": self.buff["attrs"]
                    }
                    nw.add_element(typeconv.parse(data))

                # facts
                elif self.stk == ["Network", "Facts", "Fact"]:
                    data = {
                        u"type": u"Fact",
                        u"value": self.buff["attrs"]
                    }
                    nw.add_element(typeconv.parse(data))

                # edges
                elif self.stk == ["Network", "Edges", "Edge"]:
                    data = {
                        u"type": u"Edge",
                        u"value": self.buff
                    }
                    nw.add_element(typeconv.parse(data))

                self.stk.pop()

        handler = YatelXMLHandler(self)
        sax.parse(fp, handler)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == '__main__':
    print(__doc__)

