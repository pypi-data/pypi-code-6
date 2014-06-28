from Frontier.IO.AbstractReader import AbstractReader

class NotImplementedReader(AbstractReader):

    def __init__(self, filepath, CLASSES=None, auto_close=True):
        super(NotImplementedReader, self).__init__(filepath, CLASSES, auto_close, 0)

