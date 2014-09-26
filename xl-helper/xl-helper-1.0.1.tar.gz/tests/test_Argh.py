
import sys
sys.path.append('.')

from xl_helper.Argh import Argh
import unittest
import os


class ArghTest(unittest.TestCase):

    def setUp(self):
        self.parser = Argh.createParser()

    def test_server(self):
        parsed = self.parser.parse_args('install server --version 3.9.3'.split())
        assert parsed.action == 'install'
        assert parsed.subject == 'server'
        assert parsed.plugin is None
        assert parsed.version == '3.9.3'
        assert parsed.dist is None
        assert parsed.start == False

    def test_plugin(self):
        parsed = self.parser.parse_args('install plugin tomcat --version 3.9.3'.split())
        assert parsed.action == 'install'
        assert parsed.subject == 'plugin'
        assert parsed.plugin == 'tomcat'
        assert parsed.version == '3.9.3'
        assert parsed.path == os.getcwd()
        assert parsed.dist is None
        assert parsed.start == False

    def test_location(self):
        parsed = self.parser.parse_args('install plugin tomcat --version 3.9.3 --path /path/to/xldeploy'.split())
        assert parsed.action == 'install'
        assert parsed.subject == 'plugin'
        assert parsed.plugin == 'tomcat'
        assert parsed.version == '3.9.3'
        assert parsed.path == '/path/to/xldeploy'
        assert parsed.dist is None
        assert parsed.start == False

    def test_distribution(self):
        parsed = self.parser.parse_args('install server --dist /tmp/xl-deploy-server-4.5.0.zip'.split())
        assert parsed.action == 'install'
        assert parsed.subject == 'server'
        assert parsed.dist == '/tmp/xl-deploy-server-4.5.0.zip'
        assert parsed.start == False

    def test_start(self):
        parsed = self.parser.parse_args('install server --dist /tmp/xl-deploy-server-4.5.0.zip -start'.split())
        assert parsed.action == 'install'
        assert parsed.subject == 'server'
        assert parsed.dist == '/tmp/xl-deploy-server-4.5.0.zip'
        assert parsed.start == True
