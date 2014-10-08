
from google.appengine.ext import testbed

try:
    # django 1.6 and above
    from django.test.runner import DiscoverRunner as DjangoRunner
except ImportError:
    from django.test.simple import DjangoTestSuiteRunner as DjangoRunner


class AppEngineRunnerMixin(object):
    initialize_all = False
    init_services = ["memcache", "taskqueue", "mail"]

    # https://cloud.google.com/appengine/docs/python/tools/localunittesting
    # available_services = (
    #     "blobstore",
    #     "capability",
    #     "channel",
    #     "datastore_v3",
    #     "files",
    #     "images",
    #     "logservice",
    #     "mail",
    #     "memcache",
    #     "taskqueue",
    #     "urlfetch",
    #     "user",
    #     "xmpp",
    # )

    def setup_test_environment(self, **kwargs):
        super(AppEngineRunnerMixin, self).setup_test_environment(**kwargs)

        # Need to enable the proxy stubs for AppEngine Services.
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        self._initialize_testbed_stubs()

    def _initialize_testbed_stubs(self):
        if self.initialize_all:
            self.testbed.init_all_stubs()
        else:
            for service in self.init_services:
                getattr(self.testbed, "init_{}_stub".format(service))()

    def teardown_test_environment(self, **kwargs):
        super(AppEngineRunnerMixin, self).teardown_test_environment(**kwargs)
        self.testbed.deactivate()


class AppEngineTestRunner(AppEngineRunnerMixin, DjangoRunner):
    pass
