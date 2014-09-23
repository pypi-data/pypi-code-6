#
# Test for nodes
#
#
import unittest
import dum


#
# ## Document definition
#
class Chapter:
    class dum:
        body = str, "dum_content"

    def __repr__(self):
        return "<Chapter %d>" % self.ref
DEFAULT_CHAPTER = Chapter()


class Edition:
    class dum:
        ref = 0, "dum_content"


class Document:
    class dum:
        dum_content = ""
        alone = DEFAULT_CHAPTER
        chapter = [Chapter]
        edition = [Edition]


class Page:
    class dum:
        txt = [str], "dum_content"


#
#  ## Tests
#
class TestDumContent(unittest.TestCase):
    """element's text"""

    def test_empty(self):
        S = "<document></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.alone, DEFAULT_CHAPTER)

    def test_content(self):
        S = "<document>blabla</document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.dum_content, "blabla")

    def test_content_attribute(self):
        S = "<chapter>blabla</chapter>"
        doc = dum.xmls(Chapter, S)
        self.assertEqual(doc.body, "blabla")

    def test_content_type(self):
        S = "<edition>72</edition>"
        doc = dum.xmls(Edition, S)
        self.assertEqual(doc.ref, 72)

    def test_content_multiple(self):
        S = "<page>start<chapter/>end</page>"
        doc = dum.xmls(Page, S)
        self.assertEqual(doc.txt, ["start", "end"])


if __name__ == '__main__':
    unittest.main()
