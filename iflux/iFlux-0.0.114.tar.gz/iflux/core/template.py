# Copyright 2013-2014 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from tornado.template import Loader, Template


class ModuleLoader(Loader):
    """A template loader that loads from a single root directory.
    """
    module = None

    def __init__(self, root_directory, module=None, **kwargs):
        self.module = module
        super(ModuleLoader, self).__init__(root_directory, **kwargs)

    def resolve_path(self, name, parent_path=None):
        if ':' in name:
            nameX = name.split(':')
            module_name = nameX[0]
            name = os.path.join(self.module.application.modules[module_name].get_template_path(), nameX[-1])
        return super(ModuleLoader, self).resolve_path(name, parent_path)

    def _create_template(self, name):
        path = os.path.join(self.root, name)
        f = open(path, "rb")
        template = Template(f.read(), name=name, loader=self)
        f.close()
        return template

