#
# Test for list collections
#
#
import unittest
import dum


#
# ## Document definition
#
class Chapter:
    class dum:
        ref = 0

    def __repr__(self):
        return "<Chapter %d>" % self.ref


class Document:
    class dum:
        alone = "nop"
        chapter = [Chapter]
        edition = [int]
        notype = []  # type definition default to str ..


#
#  ## Tests
#
class TestList(unittest.TestCase):
    def test_empty(self):
        S = "<document></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.alone, "nop")
        self.assertEqual(doc.chapter, [])
        self.assertEqual(doc.edition, [])

    def test_alone(self):
        S = "<document><alone>test</alone><alone>eraser</alone></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.alone, "test")

    def test_atom(self):
        S = """<document><edition>2005</edition>
               <edition>2012</edition></document>"""
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.edition, [2005, 2012])

    def test_node(self):
        S = "<document><chapter ref='1'/><chapter ref='2'/></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.chapter[0].ref, 1)
        self.assertEqual(doc.chapter[1].ref, 2)

    def test_notype(self):
        S = "<document><notype>2</notype></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.notype[0], "2")

if __name__ == '__main__':
    unittest.main()
