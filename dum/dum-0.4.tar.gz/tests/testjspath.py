#
# Test json path
#
#
import unittest
import dumxpath as xpath

values = {
    "one": {
        "value": "Hello",
        "lst": ["Hello", "World"],
    },
    "many": [{
        "value": "Hello1",
        "child": {
        }
    }, {
        "value": "Hello2",
        "key": "k1",
    }, {
        "value": "Hello3",
        "key": "k2",
    }],
}


#
#  ## Tests
#
class TestJsPath(unittest.TestCase):
    def test_one(self):
        jp = xpath.JsPath('/one/value')
        self.assertEqual(list(jp(values)), ["Hello"])
        jp = xpath.JsPath('/one/lst')
        self.assertEqual(list(jp(values)), ["Hello", "World"])

    def test_many(self):
        jp = xpath.JsPath('/many/value')
        self.assertEqual(list(jp(values)), ["Hello1", "Hello2", "Hello3"])

    def test_idx(self):
        jp = xpath.JsPath('/many[1]/value')
        self.assertEqual(list(jp(values)), ["Hello1"])

    def test_length(self):
        jp = xpath.JsPath('/many[length()]/value')
        self.assertEqual(list(jp(values)), ["Hello3"])

    def test_length_1(self):
        jp = xpath.JsPath('/many[length()-1]/value')
        self.assertEqual(list(jp(values)), ["Hello2"])

    def test_attr(self):
        jp = xpath.JsPath('/many[@key]/value')
        self.assertEqual(list(jp(values)), ["Hello2", "Hello3"])
        jp = xpath.JsPath('/many[@key=k1]/value')
        self.assertEqual(list(jp(values)), ["Hello2"])
        jp = xpath.JsPath('/many[key]/value')
        self.assertEqual(list(jp(values)), ["Hello2", "Hello3"])

    def test_parent(self):
        jp = xpath.JsPath('/many/child/../value')
        self.assertEqual(list(jp(values)), ["Hello1"])

if __name__ == '__main__':
    unittest.main()
