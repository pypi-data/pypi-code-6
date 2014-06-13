import unittest
from subprocess import check_output

class TestPythonPy(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(check_output(['pythonpy']),'')
        
    def test_numbers(self):
        self.assertEqual(check_output(['pythonpy', '3 * 4.5']),'13.5\n')

    def test_range(self):
        self.assertEqual(check_output(['pythonpy', 'range(3)']), '\n'.join(map(str, range(3))) + '\n')

    def test_range(self):
        self.assertEqual(check_output(["""echo a,b | pythonpy -x 'x[1]' --si ,"""], shell=True), 'b\n')

    def test_ignore_errors(self):
        self.assertEqual(check_output("""echo a | pythonpy -x --i 'None.None'""", shell=True), '')
        self.assertEqual(check_output("""echo a | pythonpy -fx --i 'None.None'""", shell=True), '')



if __name__ == '__main__':
    unittest.main()
