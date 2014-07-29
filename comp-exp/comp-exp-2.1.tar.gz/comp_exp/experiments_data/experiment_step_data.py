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

    def __str__(self):
        return 'ExperimentStepData <step #%d "%s">' % (self.ind, self.name)

    __repr__ = __str__
