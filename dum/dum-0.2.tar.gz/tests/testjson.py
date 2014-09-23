#
# Test json parsing
#
#
import unittest
import dum


#
# ## Document definition
#

class Action:
    class dum:
        title = ""
        value = ""


class User:
    class dum:
        name = str
        ref = 0
        numbers = [int]
        love = [Action]
        hate = Action
        size = 1.8, "ns-length"
        done = [Action], "./done",


#
#  ## Tests
#
class TestJson(unittest.TestCase):

    def test_one(self):
        jsonuser = {"name": "DUPONT", "ref": 5}
        result = dum.json(User, jsonuser)
        self.assertEqual(result.name, "DUPONT")
        self.assertEqual(result.ref, 5)

    def test_defaut(self):
        jsonuser = {}
        result = dum.json(User, jsonuser)
        self.assertFalse(hasattr(result, "name"))
        self.assertEqual(result.ref, 0)

    def test_list_one(self):
        jsonuser = {"name": "DUPONT", "numbers": 5}
        result = dum.json(User, jsonuser)
        self.assertEqual(result.numbers, [5])

    def test_list_more(self):
        jsonuser = {"name": "DUPONT", "numbers": [5, 8, 9]}
        result = dum.json(User, jsonuser)
        self.assertEqual(result.numbers, [5, 8, 9])

    def test_node_one(self):
        jsonuser = {"name": "DUPONT", "hate": {"title": "eating"}}
        result = dum.json(User, jsonuser)
        self.assertEqual(result.hate.title, "eating")

    def test_node_list(self):
        jsonuser = {"name": "DUPONT", "love": {"title": "eating"}}
        result = dum.json(User, jsonuser)
        self.assertEqual(result.love[0].title, "eating")

    def test_source(self):
        jsonuser = {"name": "DUPONT", "ns-length": 2}
        result = dum.json(User, jsonuser)
        self.assertEqual(result.size, 2.0)

    def test_xpath(self):
        jsonuser = {"name": "DUPONT",
                    "done": [{"title": "drink"}, {"title": "sleep"}]}
        result = dum.json(User, jsonuser)
        self.assertEqual(result.done[1].title, "sleep")


if __name__ == '__main__':
    unittest.main()
