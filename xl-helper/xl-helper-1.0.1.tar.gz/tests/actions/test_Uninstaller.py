import unittest
import os
import shutil

from xl_helper.Utils import Utils

from xl_helper.actions.Uninstaller import Uninstaller


class UninstallerTest(unittest.TestCase):
    server_dir = '/tmp/test-server'

    def setUp(self):
        self.uninstaller = Uninstaller()
        if os.path.isdir(self.server_dir):
            shutil.rmtree(self.server_dir)

    def tearDown(self):
        self.uninstaller = Uninstaller()
        if os.path.isdir(self.server_dir):
            shutil.rmtree(self.server_dir)

    def test_server(self):
        server_version = '4.0.0'
        full_server_path = os.path.join(self.server_dir, Utils.build_server_dir_name(server_version))
        full_server_zip_path = os.path.join(self.server_dir, Utils.build_server_zip_name(server_version))
        os.makedirs(full_server_path)
        open(full_server_zip_path, 'w+')
        assert os.path.isdir(full_server_path)
        self.uninstaller.server(server_version, self.server_dir)
        assert not os.path.isdir(full_server_path)

    def test_plugin(self):
        short_plugin_name = 'tomcat'
        plugin_version = '3.9.0'
        full_server_path = os.path.join(self.server_dir, Utils.build_server_dir_name(plugin_version))
        plugin_dir = os.path.join(full_server_path, 'plugins')
        full_plugin_path = os.path.join(plugin_dir, Utils.build_plugin_name(plugin_version, short_plugin_name))
        os.makedirs(plugin_dir)
        open(full_plugin_path, 'w+')
        self.uninstaller.plugin(short_plugin_name, plugin_version, self.server_dir)
        assert not os.makedirs(full_plugin_path)