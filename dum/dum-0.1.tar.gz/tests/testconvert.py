#
# Test for converters
#
#
import unittest
import dum


#
# ## Document definition
#
class Document:
    class dum:
        @dum.converter
        def writed(text):
            return text.replace("-", ":")

        @dum.converter(source="unprefix", default="$")
        def prefixed(text):
            return "$"+text

        @dum.lister
        def repeated(text):
            return int(text)*2

        @dum.lister(source="unsufix")
        def sufixed(text):
            return text+"%"


#
#  ## Tests
#
class TestConverter(unittest.TestCase):
    """Method conversion"""

    def test_atom_noargs(self):
        S = "<document writed='2010-2014'></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.writed, '2010:2014')

    def test_atom_args(self):
        S = "<document unprefix='a'></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.prefixed, '$a')

    def test_atom_default(self):
        S = "<document></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.prefixed, '$')

    def test_list_noargs(self):
        S = "<document><repeated>1</repeated><repeated>2</repeated></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.repeated, [2, 4])

    def test_list_args(self):
        S = "<document> <unsufix>A</unsufix><unsufix>B</unsufix> </document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.sufixed, ["A%", "B%"])

    def test_list_default(self):
        S = "<document></document>"
        doc = dum.xmls(Document, S)
        self.assertEqual(doc.sufixed, [])

if __name__ == '__main__':
    unittest.main()
