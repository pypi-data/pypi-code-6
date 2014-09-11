import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from django.test import TestCase
from sassy_coffee import compilers

class SassyCoffeeTest(TestCase):
    def test_compile_files(self):
        compilers.compile_files();