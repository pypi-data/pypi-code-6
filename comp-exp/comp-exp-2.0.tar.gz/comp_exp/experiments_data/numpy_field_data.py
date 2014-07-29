import numpy as np


class NumpyFieldData(object):

    def __init__(self, h5group, refs):
        self.group = h5group
        self.refs = refs

    @property
    def name(self):
        return self.refs.name

    @property
    def shapes(self):
        return [d.shape for d in self]

    def concat(self, axis=0):
        return np.concatenate(tuple(self), axis=axis)

    def __getitem__(self, index):
        if isinstance(index, int):
            if not 0 <= index < len(self):
                raise IndexError
            return self.group[self.refs.iloc[index]][...]
        else:
            return NumpyFieldData(self.group, self.refs[index])

    def __len__(self):
        return self.refs.map(bool).sum()

    def __str__(self):
        return 'NumpyFieldData <"%s">' % (self.name)

    __repr__ = __str__
