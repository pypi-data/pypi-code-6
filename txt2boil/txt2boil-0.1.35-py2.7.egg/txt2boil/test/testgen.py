from unittest import TestCase


class TestGen(TestCase):

    def checkGenerates(self, src, out):
        self.assertMultiLineEqual(out, self.gen(src))
        self.assertMultiLineEqual(out, self.gen(out))
