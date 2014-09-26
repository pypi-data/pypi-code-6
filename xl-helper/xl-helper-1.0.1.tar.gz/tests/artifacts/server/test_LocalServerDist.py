from xl_helper.artifacts.Cache import Cache
from xl_helper.artifacts.server.LocalServerDist import LocalServerDist
from xl_helper.artifacts.server.RemoteServerDist import RemoteServerDist
from tests.util.TestWithTempDirs import TestWithTempDirs


class LocalServerDistTest(TestWithTempDirs):

    def setUp(self):
        remote_dist = Cache.in_default_location().get(RemoteServerDist("4.0.1", self.test_config))
        self.local_server_dist = LocalServerDist(remote_dist)

    def test_should_detect_version(self):
        self.assertEqual("4.0.1", self.local_server_dist.version)

    def test_should_detect_filename(self):
        self.assertEqual("xl-deploy-4.0.1-server.zip", self.local_server_dist.get_filename())

