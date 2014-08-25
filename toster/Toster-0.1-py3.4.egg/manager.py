from importlib import import_module


class TestManager(object):

    def __init__(self):
        self.tests = {}
        self.groups = {}

    def add_testcase(self, testcase):
        testcase = self.maybe_dotted(testcase)
        key = testcase.__module__ + ':' + testcase.__name__
        self.tests[key] = testcase

        for name in testcase.groups:
            group = self.groups.get(name, [])
            group.append(testcase)
            self.groups[name] = group

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
