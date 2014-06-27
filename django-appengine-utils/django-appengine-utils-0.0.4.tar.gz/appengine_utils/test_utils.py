

from google.appengine.ext import testbed

from django.test.runner import DiscoverRunner
from django.test.simple import DjangoTestSuiteRunner


class AppEngineRunnerMixin(object):

    def setup_test_environment(self, **kwargs):
        super(AppEngineRunnerMixin, self).setup_test_environment(**kwargs)

        # Need to enable the proxy stubs for AppEngine Services.
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_memcache_stub()
        self.testbed.init_taskqueue_stub()
        self.testbed.init_mail_stub()

    def teardown_test_environment(self, **kwargs):
        super(AppEngineRunnerMixin, self).teardown_test_environment(**kwargs)
        self.testbed.deactivate()


class AppEngineTestRunner(AppEngineRunnerMixin, DjangoTestSuiteRunner):
    pass

class AppEngineDiscoverRunner(AppEngineRunnerMixin, DiscoverRunner):
    pass
