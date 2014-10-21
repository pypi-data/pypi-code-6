import unittest
import detektor


class MockFileClass(object):
    def __init__(self, filepath):
        self.path = filepath


class MockAssignment(object):
    def __init__(self, filepath):
        self.f = MockFileClass(filepath)


class TestSetSignatureOnListOfObjects(unittest.TestCase):
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
        alist = detektor.set_detektor_signature_on_list_of_objects('python', self.assignments, 'f.path')
        for a in alist:
            self.assertTrue(hasattr(a, 'detektor_signature'))

    def test_detektor_signature_set_raises_exception_on_wrong_file_path(self):
        with self.assertRaises(AttributeError):
            detektor.set_detektor_signature_on_list_of_objects(
                'python',
                self.assignments,
                'f.non_existing_path')

    def test_detektor_signature_on_object_raises_on_non_existing_file(self):
        mockass = MockAssignment('does/not/exist.py')
        assignments = [mockass, mockass]
        with self.assertRaises(IOError):
            mockass = detektor.set_detektor_signature_on_list_of_objects(
                'python', assignments, 'f.path')
