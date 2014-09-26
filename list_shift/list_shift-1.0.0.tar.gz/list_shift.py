class List(list):
    __version__ = '1.0.0'

    def shift(self):
        try:
            return self.pop(0)
        except IndexError:
            return None
