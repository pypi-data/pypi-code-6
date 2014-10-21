import os


class FileClass(object):
    def __init__(self, filepath):
        self.filepath = filepath


class Assignment(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.fileclass = FileClass(os.path.abspath(filepath))

    def __repr__(self):
        return self.filepath
