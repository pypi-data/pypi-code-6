
class Remote(object):
    def __init__(self):
        pass

    def push(self, stream, name):
        raise NotImplementedError

    def pull(self, name):
        raise NotImplementedError
