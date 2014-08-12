from .plugin import Plugin


class BeakerPlugin(Plugin):

    def get_include_name(self):
        return 'pyramid_beaker'
