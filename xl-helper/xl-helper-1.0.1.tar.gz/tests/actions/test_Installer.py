import unittest

from os import path
from xl_helper.actions.Installer import Installer
from xl_helper.artifacts.server.LocalServerDist import LocalServerDist
from xl_helper.artifacts.server.RemoteServerDist import RemoteServerDist
from tests.util.TestWithTempDirs import TestWithTempDirs


class InstallerTest(TestWithTempDirs):

    def setUp(self):
        self.installer = Installer(self.test_config)
        self.temp_dir = self.create_temp_dir()

    def test_install_server_from_local_zip(self):
        remote_dist_zip = RemoteServerDist("4.0.1", self.test_config).download(self.temp_dir)
        home = self.installer.server(LocalServerDist(path.join(self.temp_dir, remote_dist_zip)), target=self.temp_dir)
        self._assert_valid_server_installation(home)

    def test_install_server_existing_path(self):
        home = self.installer.server(RemoteServerDist('4.0.0', self.test_config), target=self.temp_dir)
        assert home.endswith('xl-deploy-4.0.0-server')
        self._assert_valid_server_installation(home)

    def test_update_server(self):
        home_3 = self.installer.server(RemoteServerDist('3.9.2', self.test_config), target=self.temp_dir)
        self.installer.plugin('was', '3.9.0', home_3)

        home_4 = self.installer.server(RemoteServerDist('4.5.0', self.test_config), target=self.temp_dir, upgrade_from_path=home_3)
        assert home_4.endswith('xl-deploy-4.5.0-server')
        self._assert_valid_server_installation(home_4)

        assert path.isfile(path.join(home_4, 'plugins/file-plugin-4.5.0.jar'))
        assert path.isfile(path.join(home_4, 'plugins/was-plugin-3.9.0.jar'))
        assert not path.isfile(path.join(home_4, 'plugins/file-plugin-3.9.2.jar'))

    def test_install_plugin(self):
        home = self.installer.server(RemoteServerDist('3.9.2', self.test_config), target=self.temp_dir)
        assert not path.isfile(path.join(home, 'plugins/jbossas-plugin-3.9.0.jar'))
        self.installer.plugin(name='jbossas', version='3.9.0', server_location=home)
        assert path.isfile(path.join(home, 'plugins/jbossas-plugin-3.9.0.jar'))

    def test_install_cli(self):
        home = self.installer.cli("3.9.4", self.create_temp_dir())
        self._assert_valid_cli_home(home)

    # Extra assertions
    def _assert_valid_server_installation(self, home):
        assert path.isfile(path.join(home, 'conf/deployit-license.lic'))
        assert path.isdir(path.join(home, 'bin'))
        assert path.isdir(path.join(home, 'lib'))
        assert path.isdir(path.join(home, 'ext'))

    def _assert_valid_cli_home(self, home):
        self.assertTrue(path.isdir(home))
        self.assertTrue(path.isfile(path.join(home, "bin", "cli.sh")))



if __name__ == '__main__':
    unittest.main()