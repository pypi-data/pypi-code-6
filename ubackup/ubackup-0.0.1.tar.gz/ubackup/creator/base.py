class Creator(object):

    @property
    def data(self):
        raise NotImplementedError

    @property
    def unique_name(self):
        raise NotImplementedError

    def create(self):
        raise NotImplementedError

    def checksum(self):
        raise NotImplementedError
