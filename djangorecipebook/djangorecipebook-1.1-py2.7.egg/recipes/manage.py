"""
Recipe generating a management script
"""

import sys
import re

from .base import BaseRecipe
from zc.buildout import easy_install


class Recipe(BaseRecipe):

    def _packages(self):
        return ['djangorecipebook']

    def __init__(self, buildout, name, options):
        super(Recipe, self).__init__(buildout, name, options)
        options.setdefault('args', '')

    def _arguments(self):
        """
        Returns the list of arguments for the djangorecipebook script
        """
        args = ''
        if self.options['args']:
            args += ', %s' % ', '.join(
                "'%s'" % d for d in re.split('\s+', self.options['args']))

        return "'%s'%s" % (self.options['settings'], args)

    def install(self):
        __, working_set = self.egg.working_set(self._packages())
        script_path = self.__class__.__module__.replace('recipes', 'scripts')
        return easy_install.scripts(
            [(self.name, script_path, 'main')],
            working_set, sys.executable, self.options['bin_dir'],
            extra_paths=self.options['extra-paths'].split(';'),
            arguments=self._arguments(),
            initialization=self._initialization())

    def update(self):
        self.install()
