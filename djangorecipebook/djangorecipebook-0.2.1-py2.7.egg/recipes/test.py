"""
Recipe generating a test script
"""

import sys

from zc.buildout import easy_install

from base import BaseRecipe


class Recipe(BaseRecipe):

    def __init__(self, buildout, name, options):
        super(Recipe, self).__init__(buildout, name, options)
        options.setdefault('apps', '')

    def install(self):
        __, working_set = self.egg.working_set(['djangorecipebook'])
        if self.options['apps']:
            apps = ', %s' % ', '.join(
                ["'%s'" % app for app in self.options['apps'].split()])
        else:
            apps = ''
        return easy_install.scripts(
            [(self.name, __name__.replace('recipes', 'scripts'), 'main')],
            working_set, sys.executable, self.options['bin_dir'],
            extra_paths=self.options['extra-paths'].split(';'),
            arguments="'%s'%s" % (self.options['settings'], apps),
            initialization=self.options['initialization'])

    def update(self):
        self.install()
