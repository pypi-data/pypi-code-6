from infi.unittest import TestCase
from infi.execute import execute_assert_success
import os
EXTENSION = '.exe' if os.name == 'nt' else ''


class CloseApplicationTestCase(TestCase):
    def test_via_buildout(self):
        execute_assert_success([os.path.join('bin', 'buildout' + EXTENSION), 'install', 'debug-logging', 'development-scripts'])
