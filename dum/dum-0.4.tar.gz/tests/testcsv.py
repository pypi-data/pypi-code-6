#
# Test csv parsing
#
#
import unittest
import dum


#
# ## Document definition
#
class User:
    class dum:
        name = "", "NAME"
        ref = int, "ID"

    def __repr__(self):
        return "<Test %s : %s>" % (self.ref, self.name)


#
#  ## Tests
#
class TestList(unittest.TestCase):
    """No prootype defined"""

    def test_header(self):
        ROWS = [("NAME", "ID"), ("DUPONT", "1"), ("DURAND", "2")]
        result = dum.csv(User, iter(ROWS))
        self.assertEqual(next(result).name, "DUPONT")
        self.assertEqual(next(result).ref, 2)

    def test_alone(self):
        ROWS = [("DUPONT", "1"), ("DURAND", "2")]
        result = dum.csv(User, iter(ROWS), headers=("NAME", "ID"))
        self.assertEqual(next(result).name, "DUPONT")
        self.assertEqual(next(result).ref, 2)

if __name__ == '__main__':
    unittest.main()
