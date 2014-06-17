import unittest
from subprocess import check_output

class TestPythonPy(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(check_output(['pythonpy']),'')
        
    def test_numbers(self):
        self.assertEqual(check_output(['pythonpy', '3 * 4.5']),'13.5\n')

    def test_range(self):
        self.assertEqual(check_output(['pythonpy', 'range(3)']), '\n'.join(map(str, range(3))) + '\n')

    def test_split_input(self):
        self.assertEqual(check_output(["""echo a,b | pythonpy -x 'x[1]' --si ,"""], shell=True), 'b\n')

    def test_split_output(self):
        self.assertEqual(check_output(["""echo abc | pythonpy -x x --si '' --so ','"""], shell=True), 'a,b,c\n')

    def test_ignore_errors(self):
        self.assertEqual(check_output("""echo a | pythonpy -x --i 'None.None'""", shell=True), '')
        self.assertEqual(check_output("""echo a | pythonpy -fx --i 'None.None'""", shell=True), '')

    def test_statements(self):
        self.assertEqual(check_output("""pythonpy -c 'a=5' -C 'print(a)'""", shell=True), '5\n')
        self.assertEqual(check_output("""echo 3 | pythonpy -c 'a=5' -x x -C 'print(a)'""", shell=True), '3\n5\n')

    def test_imports(self):
        check_output("pythonpy 'math'", shell=True)
        check_output("pythonpy 'base64'", shell=True)
        check_output("pythonpy 'calendar'", shell=True)
        check_output("pythonpy 'csv'", shell=True)
        check_output("pythonpy 'datetime'", shell=True)
        check_output("pythonpy 'hashlib'", shell=True)
        check_output("pythonpy 'glob'", shell=True)
        check_output("pythonpy 'itertools'", shell=True)
        check_output("pythonpy 'json'", shell=True)
        check_output("pythonpy 'math'", shell=True)
        check_output("pythonpy 'os'", shell=True)
        check_output("pythonpy 'random'", shell=True)
        check_output("pythonpy 're'", shell=True)
        check_output("pythonpy 'shutil'", shell=True)
        check_output("pythonpy 'tempfile'", shell=True)
        check_output("pythonpy -c 'Counter'", shell=True)
        check_output("pythonpy -c 'OrderedDict'", shell=True)
        check_output("pythonpy -c 'groupby'", shell=True)
        check_output("pythonpy 'uuid4'", shell=True)


if __name__ == '__main__':
    unittest.main()
