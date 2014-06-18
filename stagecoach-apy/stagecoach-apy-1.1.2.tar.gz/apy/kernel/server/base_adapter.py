import abc


class BaseServerAdapter():
    __metaclass__ = abc.ABCMeta

    def __init__(self, settings, dispatcher, error_handler):
        self._port = 80
        if 'port' in settings:
            self._port = settings['port']

        self._dispatcher = dispatcher
        self._error_handler = error_handler

    @abc.abstractmethod
    def run(self):
        """ runs the http server adapter """
