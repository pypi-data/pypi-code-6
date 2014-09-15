

class AttrWrapper(object):

    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)


class User(AttrWrapper):
    pass
