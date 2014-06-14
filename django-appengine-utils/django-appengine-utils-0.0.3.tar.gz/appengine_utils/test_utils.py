

from google.appengine.ext import testbed

from django.test.simple import DjangoTestSuiteRunner


class AppEngineTestRunner(DjangoTestSuiteRunner):

    def setup_test_environment(self, **kwargs):
        super(AppEngineTestRunner, self).setup_test_environment(**kwargs)

        # Need to enable the proxy stubs for AppEngine Services.
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_memcache_stub()
        self.testbed.init_taskqueue_stub()
        self.testbed.init_mail_stub()

    def teardown_test_environment(self, **kwargs):
        super(AppEngineTestRunner, self).teardown_test_environment(**kwargs)
        self.testbed.deactivate()
