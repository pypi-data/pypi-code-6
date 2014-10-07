from hatak.plugin import Plugin


class BeakerPlugin(Plugin):

    def get_include_name(self):
        return 'pyramid_beaker'

    def add_unpackers(self):
        self.unpacker.add('session', lambda req: req.session)
