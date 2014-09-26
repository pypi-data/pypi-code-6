import thread

from xl_helper.Utils import Utils
from xl_helper.actions.Installer import Installer
from xl_helper.actions.Server import Server
from xl_helper.artifacts.server.RemoteServerDist import RemoteServerDist
from tests.util.TestWithTempDirs import TestWithTempDirs


class ServerTest(TestWithTempDirs):

    def setUp(self):
        self.installer = Installer(self.test_config)
        temp_dir = self.create_temp_dir()

        home = self.installer.server(RemoteServerDist('4.0.0', self.test_config), temp_dir)
        self.server = Server(home, username="admin", password="admin", url="http://localhost:4516/deployit")

    def tearDown(self):
        self.server.stop()
        Utils.wait_until(self.server.is_stopped)

    def test_operations(self):
        assert not self.server.is_running()
        assert self.server.is_stopped()

        thread.start_new_thread(self.server.start, ())
        assert not self.server.is_running()  # still starting
        Utils.wait_until(self.server.is_running, tick=True)
        assert not self.server.is_stopped()  # has started starting

        thread.start_new_thread(self.server.restart, ())
        Utils.wait_until(self.server.is_stopped, tick=True)  # first should stop
        Utils.wait_until(self.server.is_running, tick=True)  # then should start

        self.server.stop()
        Utils.wait_until(self.server.is_stopped, tick=True)  # also takes some time
        assert not self.server.is_running()


