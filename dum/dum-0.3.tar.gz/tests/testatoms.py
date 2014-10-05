#
# Test for atomic values
#
#
import unittest
import dum


#
# ## Document definition
#
class Document:
    class dum:
        dum_content = 0
        count = 7
        size = int
        name = ""


#
#  ## Tests
#
class TestDefault(unittest.TestCase):
    """No prootype defined"""

    def test_attribute(self):
        S = "<document name='test'/>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.name, "test")

    def test_child(self):
        S = "<document><name>test</name></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.name, "test")

    def test_subtree(self):
        """subtree is ignored"""
        S = """<document><name><first>John</first>
                <last>Doe</last></name></document>"""
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.name, "")


class TestProto(unittest.TestCase):
    """With a protoype"""

    def test_attribute(self):
        S = "<document count='12'/>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.count, 12)

    def test_child(self):
        S = "<document><count>12</count></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.count, 12)

    def test_not_defined(self):
        S = "<document></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.count, 7)


class TestType(unittest.TestCase):
    """With a type"""

    def test_attribute(self):
        S = "<document size='87'/>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.size, 87)

    def test_child(self):
        S = "<document><size>50</size></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.size, 50)

    def test_content(self):
        S = "<document>87</document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.dum_content, 87)


class TestSubnode(unittest.TestCase):
    """A chld in an atomic attribute"""

    def test_child(self):
        S = "<document><size>48<child/></size></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.size, 48)

    def test_subchild(self):
        S = "<document><size>48<child><subchild/></child></size></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.size, 48)


if __name__ == '__main__':
    unittest.main()
