__author__ = 'gdoermann'

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

    def __deepcopy__(self, memo):
        dcopy = type(self)(**self)
        memo[id(self)] = dcopy
        return dcopy

