import os.path
import os
import shutil

from unittest import TestCase

from .. import main


__here__ = os.path.dirname(__file__)
examples_dir = os.path.join(__here__, 'examples')
desired_dir = os.path.join(__here__, 'desired')
work_dir = os.path.join('/tmp', 'futurify-tests')


def files_match(a, b):
    with open(a) as fa:
        with open(b) as fb:
            return fa.read() == fb.read()


class TestFull(TestCase):

    def setUp(self):
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir)
            os.makedirs(work_dir)

    def copy_examples(self, dest):
        shutil.copytree(examples_dir, dest)

    def test_dry_run_unchanged(self):
        dest = os.path.join(work_dir, 'examples')
        self.copy_examples(dest)
        main(['futurify',
              '--silent',
              '--dry-run',
              '+absolute_import', '-print_function',
              dest])
        # Check that all files are unchanged.
        for fn in ('simple.py', 'multiline.py', 'complex.py'):
            self.assertTrue(files_match(os.path.join(examples_dir, fn),
                                        os.path.join(dest, fn)))

    def test_run(self):
        dest = os.path.join(work_dir, 'examples')
        self.copy_examples(dest)
        main(['futurify',
              '--silent',
              '+absolute_import', '-print_function',
              dest])
        # Check that files are changed correctly.
        for fn in ('simple.py', 'multiline.py', 'complex.py'):
            self.assertTrue(files_match(os.path.join(desired_dir, fn),
                                        os.path.join(dest, fn)))
