import unittest
import detektor


class MockFileClass(object):
    def __init__(self, filepath):
        self.path = filepath


class MockAssignment(object):
    def __init__(self, filepath):
        self.f = MockFileClass(filepath)


class TestSetSignatureOnObject(unittest.TestCase):
    def setUp(self):
        filepath = 'detektor/tests/pyfiles/helloworldplus.py'
        self.mockassignment = MockAssignment(filepath)

    def tearDown(self):
        del self.mockassignment

    def test_detektor_signature_var_set_on_object(self):
        mockassignment = detektor.set_detektor_signature_on_single_object('python', self.mockassignment, 'f.path')
        self.assertTrue(hasattr(mockassignment, 'detektor_signature'))

    def test_detektor_signature_set_raises_exception_on_non_existing_deep_path(self):
        with self.assertRaises(AttributeError):
            detektor.set_detektor_signature_on_single_object(
                'python', 
                self.mockassignment,
                'f.non_existing_path')

    def test_detektor_signature_on_object_raises_on_non_existing_file(self):
        mockassignment = MockAssignment('does/not/exist.py')
        with self.assertRaises(IOError):
            mockassignment = detektor.set_detektor_signature_on_single_object(
                'python', mockassignment, 'f.path')
