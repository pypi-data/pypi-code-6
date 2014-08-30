from yaml import load
from importlib import import_module


class TestManager(object):

    def __init__(self, runner):
        self.tests = {}
        self.groups = {}
        self.runner = runner

    def add_testcases(self, testcases):
        for testcase in testcases:
            self.add_testcase(testcase)

    def add_testcases_from_yaml(self, path):
        with open(path, 'r') as stream:
            data = load(stream)
        for url, cls in self._inner_dict(data):
            self.add_testcase('%s:%s' % (url, cls))

    def add_testcase(self, testcase):
        testcase = self.maybe_dotted(testcase)
        key = testcase.__module__ + ':' + testcase.__name__
        self.tests[key] = testcase

        testcase.runner = self.runner

        for name in testcase.groups:
            group = self.groups.get(name, [])
            group.append(testcase)
            self.groups[name] = group

    def _inner_dict(self, data, prefix=''):
        if data is None:
            return
        for name, value in data.items():
            if value is None:
                continue
            elif type(value) is dict:
                yield from self._inner_dict(value, prefix + name + '.')
            else:
                for element in value:
                    yield (prefix + name, element)

    def maybe_dotted(self, testcase):
        if type(testcase) is not str:
            return testcase

        package_url, class_name = testcase.split(':')
        package = import_module(package_url)
        return getattr(package, class_name)

    def get_by_name(self, name):
        return [
            testcase
            for fullname, testcase in self.tests.items()
            if fullname.split(':')[1] == name
        ]

    def get_by_group(self, name):
        return self.groups[name]

    def get_by_module(self, module):
        return [
            testcase
            for fullname, testcase in self.tests.items()
            if fullname.startswith(module)
        ]

    def get_all(self):
        return self.tests.values()
