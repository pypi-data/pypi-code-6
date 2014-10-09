from zc.recipe.egg import Egg


class Recipe(Egg):

    def __init__(self, buildout, name, options):
        self.options = options
        name = 'ftw.recipe.checkversions'

        # Only install "bin/masstranslate" script, not other scripts.
        options['scripts'] = 'checkversions'

        blacklists = options.get('blacklists')
        blacklists = blacklists and blacklists.split() or []
        blacklist_packages = options.get('blacklist-packages')
        blacklist_packages = (blacklist_packages and
                              blacklist_packages.split() or [])

        kwargs = {'buildout_dir': buildout['buildout']['directory'],
                  'versions': options.get('versions', 'versions.cfg'),
                  'blacklists': blacklists,
                  'blacklist_packages': blacklist_packages,
                  'index': options.get('index', None)}

        relative_paths = buildout['buildout'].get('relative-paths', 'false') == 'true'
        if relative_paths:
            # With relative-paths, there is a "base" variable containing
            # the buildout path.
            buildout_dir_arg = "'buildout_dir': base,\n"
        else:
            buildout_dir_arg = "'buildout_dir': {buildout_dir!r},\n".format(**kwargs)

        args_string = ("**{{" +
                       buildout_dir_arg +
                       "'versions': {versions!r},\n"
                       "'blacklists': {blacklists!r},\n"
                       "'blacklist_packages': {blacklist_packages!r},\n"
                       "'index': {index!r},\n"
                       "}}").format(**kwargs)

        options['arguments'] = args_string


        super(Recipe, self).__init__(buildout, name, options)
