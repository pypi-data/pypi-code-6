#
# Test for xml namespaces
#
#
import unittest
import dum


#
# ## Document definition
#
class Info:
    class dum:
        __namespaces__ = {"a": "http://n1.org", "b": "http://n2.org"}
        infoN1 = "", "a:info"
        infoN2 = "", "b:info"


class InfoN2:
    class dum:
        __default_namespace__ = "http://n2.org"
        info = ""

XML = """<root xmlns:a="http://n1.org"
  xmlns:b="http://n2.org">
<a:info>Hello</a:info>
<b:info>World</b:info>
</root>"""


#
#  ## Tests
#
class TestNamespace(unittest.TestCase):
    def test_explicit(self):
        doc = dum.xmls(Info, XML)
        self.assertEqual(doc.infoN1, "Hello")
        self.assertEqual(doc.infoN2, "World")

    def test_default(self):
        doc = dum.xmls(InfoN2, XML)
        self.assertEqual(doc.info, "World")


if __name__ == '__main__':
    unittest.main()
