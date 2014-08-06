import pkg_resources
from os.path import join

import tornado.template

class PexTemplateLoader(tornado.template.BaseLoader):
    def __init__(self, module, resource_path = None, **kwargs):
        super(PexTemplateLoader,self).__init__(**kwargs)
        self.module = module
        self.resource_path = resource_path

    def load(self, name, parent_path=None):
        path = join(self.resource_path, name)if self.resource_path else name
        template = tornado.template.Template(
            pkg_resources.resource_string(self.module, path),
            name=name,
            loader=self
        )

        with self.lock:
            if name not in self.templates:
                self.templates[name] = template
            return self.templates[name]
