import pandas as pd
from .numpy_field_data import NumpyFieldData


class ExperimentStepData(object):

    def __init__(self, h5group):
        self.group = h5group

    @property
    def ind(self):
        return self.group.attrs['ind']

    @property
    def name(self):
        return self.group.attrs['name']

    @property
    def attrs(self):
        return self.group.attrs

    @property
    def completed_count(self):
        return self.group['scalars'].attrs['written_cnt']

    @property
    def full_df(self):
        df = pd.DataFrame(self.group['scalars'][...])
        return df

    @property
    def scalars_df(self):
        df = self.full_df
        columns = df.dtypes[df.dtypes != object].index
        return df[columns]

    @property
    def numpy_fields(self):
        df = self.full_df
        columns = df.dtypes[df.dtypes == object].index
        return {colname: NumpyFieldData(self.group, df[colname])
                for colname in columns}

    def concat_add_all_scalars(self, npf_data, npf_to_df=lambda npf_arr: pd.DataFrame(npf_arr)):
        scalars_subdf = self.scalars_df.loc[npf_data.refs.index]
        lst_to_concat = []

        for scalars_row, npf_arr in zip(scalars_subdf.itertuples(index=False), npf_data):
            inner_df = npf_to_df(npf_arr)
            for i, (colname, val) in enumerate(zip(self.scalars_df.columns, scalars_row)):
                inner_df.insert(i, colname, val)
            lst_to_concat.append(inner_df)

        return pd.concat(lst_to_concat)

    def __str__(self):
        return 'ExperimentStepData <step #%d "%s">' % (self.ind, self.name)

    __repr__ = __str__
