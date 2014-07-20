"""
Recipe generating a management script
"""

import sys

from base import BaseRecipe
from zc.buildout import easy_install


class Recipe(BaseRecipe):

    def install(self):
        __, working_set = self.egg.working_set(['djangorecipebook'])
        return easy_install.scripts(
            [(self.name, __name__.replace('recipes', 'scripts'), 'main')],
            working_set, sys.executable, self.options['bin_dir'],
            extra_paths=self.options['extra-paths'].split(';'),
            arguments="'%s'" % self.options['settings'],
            initialization=self.options['initialization'])

    def update(self):
        self.install()
