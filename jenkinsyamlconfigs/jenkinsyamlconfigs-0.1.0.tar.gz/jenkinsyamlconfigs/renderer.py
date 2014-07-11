
import os
import yaml
import jinja2
from pyul import coreUtils

__all__ = ['Renderer']

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
YAML_DIR = os.path.join(BASE_DIR, 'yaml')
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')

class Loader(yaml.Loader):

    def insert(self, node):
        '''Adds the contents of a file to the current Yaml File'''
        filename = os.path.join(SCRIPTS_DIR, self.construct_scalar(node))

        with open(filename, 'r') as f:
            return f.read()
        
    def include(self, node):
        '''Add Another Yaml file to the current Yaml File'''
        filename = os.path.join(YAML_DIR, self.construct_scalar(node))

        with open(filename, 'r') as f:
            return yaml.load(f, Loader)

Loader.add_constructor('!insert', Loader.insert)
Loader.add_constructor('!include', Loader.include)

class JobConfig(coreUtils.YAMLConfig):
    
    def parse(self, data):
        '''Overrides the yaml loader'''
        return yaml.load(data, Loader)


class Renderer(object):
    def __init__(self):
        pass
    
    def set_templates_dir(self, filepath):
        global TEMPLATES_DIR
        TEMPLATES_DIR = filepath
        
    def set_yaml_dir(self, filepath):
        global YAML_DIR
        YAML_DIR = filepath
        
    def set_scripts_dir(self, filepath):
        global SCRIPTS_DIR
        SCRIPTS_DIR = filepath
        
    def get_jinja_env(self):       
        return jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=TEMPLATES_DIR),
                                  extensions=['jinja2.ext.with_'],
                                  trim_blocks=True,
                                  lstrip_blocks=True,
                                  autoescape=True)
    
    def get_template(self, template_name):
        jinja = self.get_jinja_env()
        return jinja.get_template(template_name + '.xml')
        
    def get_context(self, context_name):
        filepath = os.path.join(YAML_DIR, context_name + '.yml')
        return JobConfig(filepath)
        
    def get_job_xml(self, context):
        template = self.get_template('job')
        return template.render({'job':context})


