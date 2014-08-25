from argparse import ArgumentParser
import unittest


class TestRunner(object):

    def __init__(self, manager):
        self.manager = manager
        self.loader = unittest.TestLoader()
        self.verbosity = 1
        self.args = None

    def create_suite(self):
        test_cases = [
            self.loader.loadTestsFromTestCase(test_case)
            for test_case in self.get_tests()
        ]
        return unittest.TestSuite(test_cases)

    def get_tests(self):
        if self.args.case:
            return self.manager.get_by_name(self.args.case)
        elif self.args.group:
            return self.manager.get_by_group(self.args.group)
        else:
            return self.manager.get_all()

    def create_parser(self):
        if self.args is not None:
            return

        self.parser = ArgumentParser(
            description='Run some tests.')
        self.parser.add_argument(
            '-c', '--case',
            dest='case',
            help='specify which test case')
        self.parser.add_argument(
            '-g', '--group',
            dest='group',
            help='specify which group to run')
        self.parser.add_argument(
            '-l', '--list',
            dest='list',
            action='store_true',
            help='list all tests and groups')
        self.args = self.parser.parse_args()

    def run(self):
        suite = self.create_suite()
        unittest.TextTestRunner(verbosity=self.verbosity).run(suite)

    def print_list(self):
        print('Cases:')
        print('\t' + '\n\t'.join(self.manager.tests.keys()))
        print('Groups:')
        print('\t' + '\n\t'.join(self.manager.groups.keys()))

    def __call__(self):
        self.create_parser()
        if self.args.list:
            self.print_list()
        else:
            self.run()
