from .base import ExperimenterBase

class ExperimenterPure(ExperimenterBase):

    def init_results(self):
        self.results = [[] for _ in range(len(self.steps))]

    def add_result(self, step_ind, args, result):
        self.results[step_ind].append({'args': args, 'res': result})
