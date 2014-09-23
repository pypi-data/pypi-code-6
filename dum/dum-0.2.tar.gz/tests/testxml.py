#
# Test xml parsing
#
#
import io
import unittest
import dum


#
# ## Document definition
#
class Action:
    class dum:
        title = ""
        value = ""
        inchild = "", "./prop"  # collect value only on children
        inattr = "", "./@prop"  # ... or on attributes


class User:
    class dum:
        name = str
        ref = 0
        numbers = [int]
        love = [Action]
        hate = Action
        size = 1.8, "ns-length"
        done = [Action], "./done/action"


#
#  ## Tests
#
class TestXml(unittest.TestCase):
    def test_one(self):
        xmluser = "<user><name>DUPONT</name><ref>5</ref></user>"
        result = dum.xmls(User, xmluser)
        self.assertEqual(result.name, "DUPONT")
        self.assertEqual(result.ref, 5)

    def test_defaut(self):
        xmluser = "<user></user>"
        result = dum.xmls(User, xmluser)
        self.assertFalse(hasattr(result, "name"))
        self.assertEqual(result.ref, 0)

    def test_list_one(self):
        xmluser = "<user><name>DUPONT</name><numbers>5</numbers></user>"
        result = dum.xmls(User, xmluser)
        self.assertEqual(result.numbers, [5])

    def test_list_more(self):
        xmluser = """<user><name>DUPONT</name><numbers>5</numbers>
                     <numbers>8</numbers><numbers>9</numbers></user>"""
        result = dum.xmls(User, xmluser)
        self.assertEqual(result.numbers, [5, 8, 9])

    def test_node_one(self):
        xmluser = """<user><name>DUPONT</name><hate>
                     <title>eating</title></hate></user>"""
        result = dum.xmls(User, xmluser)
        self.assertEqual(result.hate.title, "eating")

    def test_node_list(self):
        xmluser = """<user><name>DUPONT</name><love>
                     <title>eating</title></love></user>"""
        result = dum.xmls(User, xmluser)
        self.assertEqual(result.love[0].title, "eating")

    def test_source(self):
        xmluser = "<user><name>DUPONT</name><ns-length>2</ns-length></user>"
        result = dum.xmls(User, xmluser)
        self.assertEqual(result.size, 2.0)

    def test_xpath(self):
        xmluser = """<user><name>DUPONT</name><done>
                        <action><title>drink</title></action>
                        <action><title>sleep</title></action></done></user>"""
        result = dum.xmls(User, xmluser)
        self.assertEqual(result.done[1].title, "sleep")

    def test_attr(self):
        xmluser = """<user><love><prop>drink</prop></love>
                        <love prop="sleep"/></user>"""
        result = dum.xmls(User, xmluser)
        self.assertEqual(result.love[0].inattr, "")
        self.assertEqual(result.love[0].inchild, "drink")

        self.assertEqual(result.love[1].inattr, "sleep")
        self.assertEqual(result.love[1].inchild, "")

    def test_file(self):
        xmluser = "<user><name>DUPONT</name><ref>5</ref></user>"
        xmlfile = io.StringIO(xmluser)
        result = dum.xml(User, xmlfile)
        self.assertEqual(result.name, "DUPONT")
        self.assertEqual(result.ref, 5)


if __name__ == '__main__':
    unittest.main()
