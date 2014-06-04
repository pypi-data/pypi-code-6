from pybuilder.terminal import print_text


def test_proxy_for(project):
    if project.get_property('teamcity_output') and not project.get_property('__running_coverage'):
        return TeamCityTestProxy()
    else:
        return TestProxy()


def flush_text_line(text_line):
    print_text(text_line + '\n', flush=True)


class TestProxy(object):

    def __init__(self, test_name='not set'):
        self.test_name = test_name

    def and_test_name(self, test_name):
        self.test_name = test_name
        return self

    def test_starts(self):
        pass

    def test_finishes(self):
        pass

    def fails(self, reason):
        pass

    def __enter__(self, *args, **kwargs):
        self.test_starts()
        return self

    def __exit__(self, *args, **kwargs):
        self.test_finishes()


class TeamCityTestProxy(TestProxy):

    def test_starts(self):
        flush_text_line("##teamcity[testStarted name='{0}']".format(self.test_name))

    def test_finishes(self):
        flush_text_line("##teamcity[testFinished name='{0}']".format(self.test_name))

    def fails(self, reason):
        flush_text_line("##teamcity[testFailed name='{0}' message='See details' details='{1}']".format(
                        self.test_name,
                        reason
                        ))
