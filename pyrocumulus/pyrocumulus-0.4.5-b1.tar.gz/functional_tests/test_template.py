# -*- coding: utf-8 -*-

import os
import sys
import requests
from pyrocumulus.testing import TornadoApplicationTestCase
from pyrocumulus.web.handlers import TemplateHandler
from pyrocumulus.web.urlmappers import URLSpec
from pyrocumulus.web.applications import Application
from pyrocumulus.conf import settings


class MyHandler(TemplateHandler):
    def get(self):
        self.render_template('test.html', {'whoareyou': 'weareus'})


url = URLSpec('/template$', MyHandler)
application = Application(url_prefix='', handlerfactory=lambda: None,
                          extra_urls=[url])


class TemplateTestCase(TornadoApplicationTestCase):
    # exclude it from examples
    @classmethod
    def setUpClass(cls):
        cls.python_exec = cls._get_python_exec()
        cls.application = 'functional_tests.test_template.application'
        super(TemplateTestCase, cls).setUpClass()

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

    def test_render_template(self):
        url = settings.BASE_URL + '/template'
        response = requests.get(url)
        response.connection.close()
        self.assertEqual(response.status_code, 200)
