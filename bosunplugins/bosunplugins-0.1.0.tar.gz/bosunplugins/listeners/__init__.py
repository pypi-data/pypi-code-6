from .ftp import FTPListener
from .http import HTTPListener


class Listeners(object):
    def __init__(self):
        self.classes = {
            'http': HTTPListener,
            'ftp': FTPListener,
        }

    def __getattr__(self, name):
        # if it's in the list of classes, instantiate it and save as attr
        if name in self.classes:
            listener_instance = self.classes[name]()
            setattr(self, name, listener_instance)
            return listener_instance

        # if it's not, raise the original AttributeError
        raise AttributeError("type object 'Listeners' has no attribute " + name)
