from .base import ExperimenterBase
from ..common import get_column_tuples
import pandas as pd

class ExperimenterPandas(ExperimenterBase):

    def init_results(self):
        self.results = [pd.DataFrame(columns=pd.MultiIndex.from_tuples(get_column_tuples(self.steps[:i+1]), names=('type', 'step', 'name')))
                        for i in range(len(self.steps))]

    def add_result(self, step_ind, args, result):
        row = args.copy()
        row.update(result)

        df = self.results[step_ind]
        row = [row[k] for k in df.columns.get_level_values('name')]
        df.loc[len(df)] = row
