import unittest
from subprocess import check_output

class TestPythonPy(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(check_output(['py']),'')
        
    def test_numbers(self):
        self.assertEqual(check_output(['py', '3 * 4.5']),'13.5\n')

    def test_range(self):
        self.assertEqual(check_output(['py', 'range(3)']), '\n'.join(map(str, range(3))) + '\n')

    def test_split_input(self):
        self.assertEqual(check_output(["""echo a,b | py -x 'x[1]' --si ,"""], shell=True), 'b\n')

    def test_split_output(self):
        self.assertEqual(check_output(["""echo abc | py -x x --si '' --so ','"""], shell=True), 'a,b,c\n')

    def test_ignore_errors(self):
        self.assertEqual(check_output("""echo a | py -x --i 'None.None'""", shell=True), '')
        self.assertEqual(check_output("""echo a | py -fx --i 'None.None'""", shell=True), '')

    def test_statements(self):
        self.assertEqual(check_output("""py -c 'a=5' -C 'print(a)'""", shell=True), '5\n')
        self.assertEqual(check_output("""echo 3 | py -c 'a=5' -x x -C 'print(a)'""", shell=True), '3\n5\n')

    def test_imports(self):
        check_output("py 'math'", shell=True)
        check_output("py 'base64'", shell=True)
        check_output("py 'calendar'", shell=True)
        check_output("py 'csv'", shell=True)
        check_output("py 'datetime'", shell=True)
        check_output("py 'hashlib'", shell=True)
        check_output("py 'glob'", shell=True)
        check_output("py 'itertools'", shell=True)
        check_output("py 'json'", shell=True)
        check_output("py 'math'", shell=True)
        check_output("py 'os'", shell=True)
        check_output("py 'random'", shell=True)
        check_output("py 're'", shell=True)
        check_output("py 'shutil'", shell=True)
        check_output("py 'tempfile'", shell=True)
        check_output("py -c 'Counter'", shell=True)
        check_output("py -c 'OrderedDict'", shell=True)
        check_output("py -c 'groupby'", shell=True)
        check_output("py 'uuid4'", shell=True)


if __name__ == '__main__':
    unittest.main()
