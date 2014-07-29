import numpy as np
import pandas as pd


class NumpyFieldData(object):

    def __init__(self, h5group, refs, mapfunc=lambda i, arr: arr):
        self.group = h5group
        self.refs = refs
        self.mapfunc = mapfunc

    def as_df_field(self):
        return DFFieldData(self.group, self.refs, lambda i, arr: pd.DataFrame(self.mapfunc(i, arr)))

    @property
    def name(self):
        return self.refs.name

    @property
    def shapes(self):
        return [d.shape for d in self]

    def concat(self, axis=0):
        return np.concatenate(list(self), axis=axis)

    def map(self, func):
        return self.mapi(lambda i, arr: func(arr))

    def mapi(self, func):
        return self.__class__(self.group, self.refs, mapfunc=lambda i, arr: func(i, self.mapfunc(i, arr)))

    def __getitem__(self, index):
        if isinstance(index, int):
            if not 0 <= index < len(self):
                raise IndexError
            ref_ind = self.refs.index[index]
            return self.mapfunc(ref_ind, self.group[self.refs.iloc[index]][...])
        elif isinstance(index, tuple):
            def mapf(arr):
                for s in index[1:]:
                    arr = arr[s]
                return arr
            return self[index[0]].map(mapf)
        else:
            return self.__class__(self.group, self.refs[index], self.mapfunc)

    def __len__(self):
        # non-null HDF5 references
        return self.refs.map(bool).sum()

    def __str__(self):
        return 'NumpyFieldData <"%s">' % (self.name)

    __repr__ = __str__


class DFFieldData(NumpyFieldData):

    def with_outer_ind(self):

        def mapf(i, df):
            df.index.name = 'inner'
            df['outer'] = i
            df.set_index('outer', append=True, inplace=True)
            df = df.reorder_levels(['outer', 'inner'])
            return df

        return self.mapi(mapf)

    def concat(self, axis=0):
        return pd.concat(list(self), axis=axis)

    def merge_with_scalars(self, step):
        concatenated = self.with_outer_ind().concat()
        scalars = step.scalars_df
        scalars.index.name = 'outer'
        return scalars.join(concatenated, how='right')

    def __str__(self):
        return 'DFFieldData <"%s">' % (self.name)

    __repr__ = __str__
