import unittest
import detektor


class MockFileClass(object):
    def __init__(self, filepath):
        self.path = filepath


class MockAssignment(object):
    def __init__(self, filepath):
        self.f = MockFileClass(filepath)


class TestSetSignatureOnListOfObjectsOrObject(unittest.TestCase):
    def setUp(self):
        filepath = 'detektor/tests/pyfiles/helloworldplus.py'
        self.mockassignment = MockAssignment(filepath)
        self.assignments = [
            self.mockassignment,
            self.mockassignment,
        ]

    def tearDown(self):
        del self.mockassignment

    def test_detektor_signature_var_set_on_list_of_objects(self):
        alist = detektor.set_detektor_signature('python', self.assignments, 'f.path')
        for a in alist:
            self.assertTrue(hasattr(a, 'detektor_signature'))

    def test_detektor_signature_var_set_on_object(self):
        a = detektor.set_detektor_signature('python', self.mockassignment, 'f.path')
        self.assertTrue(hasattr(a, 'detektor_signature'))
