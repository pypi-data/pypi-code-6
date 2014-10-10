#
# This is a work in progress :
#   - Generating dum classes skeleton from xml schema
#   - Inferring type information to make type declaration shorter ?

import sys
sys.path.append('.')
import dum


class Atom:
    def __repr__(self):
        return "%s:%s" % (self.name, self.type)


class Sequence:
    def __repr__(self):
        return "%s(%s)" % (self.name, ", ".join(repr(x) for x in self.childs))


class Element:
    class dum:
        type = ""
        name = ""

    def dum_projection(self):
        if self.sequence:
            obj = Sequence()
            obj.childs = self.sequence
        else:
            obj = Atom()
            obj.type = self.type[3:]  # remove xs:
        obj.name = self.name
        return obj
Element.dum.sequence = [Element], "complexType/sequence/element"


class Schema:
    class dum:
        __default_namespace__ = "http://www.w3.org/2001/XMLSchema"
        element = [Element]

    def __repr__(self):
        return "\n".join(repr(s) for s in self.element)


SCHEMA = """
  <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="personne">
      <xs:complexType>
        <xs:sequence>
          <xs:element name="nom" type="xs:string" />
          <xs:element name="prenom" type="xs:string" />
          <xs:element name="date_naissance" type="xs:date" />
          <xs:element name="etablissement" type="xs:string" />
          <xs:element name="num_tel" type="xs:string" />
        </xs:sequence>
      </xs:complexType>
    </xs:element>
  </xs:schema>
"""

doc = dum.xmls(Schema, SCHEMA)
print(doc)
