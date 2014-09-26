import unittest
import os

from xl_helper.Utils import Utils
from tests.util.TestingUtils import TestingUtils


class UtilsTest(unittest.TestCase):

    config = TestingUtils.get_test_config()
    downloads_username = config.get('downloads', 'username')
    downloads_password = config.get('downloads', 'password')

    def test_build_url_for_servers(self):
        expected_path = 'https://tech.xebialabs.com/download/xl-deploy/4.0.0/xl-deploy-4.0.0-server.zip'
        assert expected_path == Utils.build_url('4.0.0', 'server')

        expected_path = 'https://tech.xebialabs.com/download/deployit/3.9.4/deployit-3.9.4-server.zip'
        assert expected_path == Utils.build_url('3.9.4', 'server')

    def test_build_url_for_plugins(self):
        expected_path = 'https://tech.xebialabs.com/download/plugins/tomcat-plugin/3.9.2/tomcat-plugin-3.9.2.jar'
        assert expected_path == Utils.build_url('3.9.2', 'plugin', 'tomcat')

        expected_path = 'https://tech.xebialabs.com/download/plugins/ec2-plugin/4.0.0-beta-3/ec2-plugin-4.0.0-beta-3.jar'
        assert expected_path == Utils.build_url('4.0.0-beta-3', 'plugin', 'ec2')

        expected_path = 'https://tech.xebialabs.com/download/plugins/xl-scale-plugin/4.0.0/xl-scale-plugin-4.0.0.jar'
        assert expected_path == Utils.build_url('4.0.0', 'plugin', 'xl-scale')

    def test_download_file(self):
        version = '4.0.0'
        file_name = 'xl-deploy-4.0.0-server.zip.md5'
        url = 'https://tech.xebialabs.com/download/xl-deploy/%s/%s' % (version, file_name)
        target = '/tmp/'

        target_file = Utils.download(url, target, self.downloads_username, self.downloads_password)
        assert os.path.isfile(target_file), 'file %s hasn\'t been found' % target_file
        os.remove(target_file)

    def test_download_plugin(self):
        tomcat_url = Utils.build_url('4.0.0-beta-3', 'plugin', 'ec2')
        target_file = Utils.download(tomcat_url, os.getcwd(), self.downloads_username, self.downloads_password)
        os.remove(target_file)

    def test_build_urls_for_cli(self):
        self.assertEqual(
            'https://tech.xebialabs.com/download/xl-deploy/4.0.0/xl-deploy-4.0.0-cli.zip',
            Utils.build_url('4.0.0', 'cli')
        )
        self.assertEqual(
            'https://tech.xebialabs.com/download/deployit/3.9.4/deployit-3.9.4-cli.zip',
            Utils.build_url('3.9.4', 'cli')
        )


if __name__ == '__main__':
    unittest.main()