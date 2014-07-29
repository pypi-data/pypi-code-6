from .experiment_step_data import ExperimentStepData


class ExperimentData(object):

    def __init__(self, h5group):
        self.group = h5group

    @property
    def time(self):
        return self.group.attrs['time_sec']

    @property
    def time_str(self):
        return self.group.attrs['time_str']

    @property
    def name(self):
        return self.group.attrs['name']

    @property
    def attrs(self):
        return self.group.attrs

    @property
    def steps(self):
        steps_groups = self.group.values()
        steps = map(ExperimentStepData, steps_groups)
        return sorted(steps, key=lambda s: s.ind)

    def __str__(self):
        return 'ExperimentData <"%s" at %s>' % (self.name, self.time_str)

    __repr__ = __str__
