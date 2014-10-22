# coding=utf-8

import os
import codecs
from weppy.extensions import Extension, TemplateExtension
from .hamlpy import Compiler


class Haml(Extension):
    namespace = 'Haml'
    default_config = dict(
        set_as_default=False
    )

    def _load_config(self):
        self.config.set_as_default = self.config.get(
            'set_as_default', self.default_config['set_as_default'])

    def on_load(self):
        self._load_config()
        self.app.add_template_extension(HamlTemplate)
        if self.config.set_as_default:
            self.app.template_default_extension = '.haml'
        for path, dirs, files in os.walk(self.app.template_path):
            for fname in files:
                if os.path.splitext(fname)[1] == ".haml":
                    filepath = os.path.join(path, fname)
                    self.process(filepath)

    def process(self, filepath):
        haml_lines = codecs.open(
            filepath, 'r',
            encoding='utf-8').read().splitlines()
        compiler = Compiler()
        output = compiler.process_lines(haml_lines)
        outfile = codecs.open(filepath+".html", 'w', encoding='utf-8')
        outfile.write(output)


class HamlTemplate(TemplateExtension):
    namespace = 'Haml'
    file_extension = '.haml'

    def preload(self, path, name):
        return path, name+".html"
