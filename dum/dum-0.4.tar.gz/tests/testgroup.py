#
# Test for group collections
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
        content = dum.group(chapter=Chapter, intro=str, dum_content=str)


#
#  ## Tests
#
class TestGroup(unittest.TestCase):
    """ """

    def test_empty(self):
        S = "<document></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.content, [])

    def test_multi(self):
        S = "<document><intro>an introduction</intro>"\
            "<chapter ref='1'/><chapter ref='2'/></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.content[0], u'an introduction')
        self.assertEqual(doc.content[1].ref, 1)
        self.assertEqual(doc.content[2].ref, 2)

    def test_content(self):
        S = """<document>some text<chapter ref='1'/>other text</document>"""
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.content[0], u'some text')
        self.assertEqual(doc.content[1].ref, 1)
        self.assertEqual(doc.content[2], u'other text')

if __name__ == '__main__':
    unittest.main()
