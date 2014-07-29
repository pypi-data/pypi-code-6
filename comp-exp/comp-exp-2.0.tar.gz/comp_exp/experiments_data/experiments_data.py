import h5py
from .experiment_data import ExperimentData


class ExperimentsData(object):

    def __init__(self, h5fname):
        self.h5file = h5py.File(h5fname, mode='r')

    @property
    def experiments(self):
        groups = [group
                  for group in ed.h5file.values()
                  if group.attrs.get('_is_experiment', False)]
        experiments = map(ExperimentData, groups)
        return sorted(experiments, key=lambda e: e.time)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.h5file.close()
