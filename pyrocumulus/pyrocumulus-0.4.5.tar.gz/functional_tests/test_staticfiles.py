# -*- coding: utf-8 -*-

import os
import sys
import requests
from pyrocumulus.testing import TornadoApplicationTestCase
from pyrocumulus.conf import settings
from pyrocumulus.web.applications import StaticApplication

application = StaticApplication()


class StaticFileTestCase(TornadoApplicationTestCase):
    # exclude it from examples
    @classmethod
    def setUpClass(cls):
        cls.python_exec = cls._get_python_exec()
        cls.application = 'functional_tests.test_staticfiles.application'
        super(StaticFileTestCase, cls).setUpClass()

    @classmethod
    def _get_python_exec(cls):
        # hack to call the correct intepreter on
        # buildbot.

        env = [p for p in sys.argv if '--tornadoenv=' in p]
        if env:
            env = env[0].split('=')[1]
        else:
            return 'python'
        return os.path.join(env, os.path.join('bin', 'python'))

    def setUp(self):
        self.static_url = settings.BASE_URL + settings.STATIC_URL

    def test_get_static_file(self):
        filename = 'test.js'
        url = self.static_url + filename
        response = requests.get(url)
        response.connection.close()
        self.assertEqual(response.status_code, 200)
