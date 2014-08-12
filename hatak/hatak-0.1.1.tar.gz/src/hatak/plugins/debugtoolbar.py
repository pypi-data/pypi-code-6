from .plugin import Plugin


class DebugtoolbarPlugin(Plugin):

    def get_include_name(self):
        if self.settings['debug']:
            return 'pyramid_debugtoolbar'
        else:
            raise NotImplementedError()
