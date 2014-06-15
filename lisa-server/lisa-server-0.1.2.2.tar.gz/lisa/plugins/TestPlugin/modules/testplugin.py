# -*- coding: UTF-8 -*-
from lisa.server.plugins.IPlugin import IPlugin
import gettext
import inspect
import os

class TestPlugin(IPlugin):
    def __init__(self):
        super(TestPlugin, self).__init__()
        self.configuration_plugin = self.mongo.lisa.plugins.find_one({"name": "TestPlugin"})
        self.path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
            inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
        self._ = translation = gettext.translation(domain='testplugin',
                                                   localedir=self.path,
                                                   fallback=True,
                                                   languages=[self.configuration_lisa['lang']]).ugettext

    def sayHello(self, jsonInput):
        return {"plugin": "TestPlugin",
                "method": "sayHello",
                "body": self._('Hello. How are you ?')
        }
