"""
Defines the base recipe for all recipes of the recipe book
"""

import os
from zc.recipe.egg import Egg


class BaseRecipe(object):

    def __init__(self, buildout, name, options):

        # recipe book's egg
        self.egg = Egg(buildout, options['recipe'].split(':')[0], options)

        self.buildout, self.name, self.options = buildout, name, options

        options['root_dir'] = self.buildout['buildout']['directory']

        # extraction of buildout parameters
        options['bin_dir'] = self.buildout['buildout']['bin-directory']

        # extraction of common options
        proj_dir = options.get('project-dir', '.')
        options['proj_dir'] = os.path.normpath(
            os.path.join(options['root_dir'], proj_dir))
        options.setdefault('settings', 'settings')
        options.setdefault('initialization', '')

        extra_paths = [options['root_dir']]
        if proj_dir != '.':
            extra_paths.append(self.options['proj_dir'])
        for path in options.get('extra-paths', '').splitlines():
            path = path.strip()
            if path:
                extra_paths.append(os.path.normpath(path))
        options['extra-paths'] = ';'.join(extra_paths)
