import logging.config

from .plugin import Plugin


class LoggingPlugin(Plugin):

    def before_config(self):
        logging.config.fileConfig(
            self.settings['logging:config'],
            disable_existing_loggers=False)
