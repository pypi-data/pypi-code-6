import copy

from zopeskel.plone import BasicZope
from zopeskel.base import get_var
from zopeskel.base import var


class Bootstrap(BasicZope):
    _template_dir = 'templates/bootstrap'
    summary = "Diazo Bootstrap Theme package with less and js resources"
    help = """
"""
    category = "Plone Development"
    required_templates = ['basic_namespace']
    use_local_commands = False
    use_cheetah = True
    vars = copy.deepcopy(BasicZope.vars)
    get_var(vars, 'namespace_package').default = 'diazotheme'
    get_var(vars, 'package').default = 'bootstrap'
    get_var(vars, 'description').default = 'Diazo Bootstrap Theme Package'
    get_var(vars, 'license_name').default = 'GPL version 2'

    def pre(self, command, output_dir, vars):
        vars['include_doc'] = True

