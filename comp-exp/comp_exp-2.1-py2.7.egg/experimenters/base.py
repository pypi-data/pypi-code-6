import inspect
from ipy_progressbar import ProgressBar


class ExperimenterBase(object):

    def __init__(self, **kwargs):
        self.steps = self.get_steps()
        self.__dict__.update(kwargs)

    def get_steps(self):
        steps = inspect.getmembers(self, predicate=lambda m: getattr(m, '_is_step', False))
        steps = dict(steps).values()
        steps_sorted = []
        while len(steps_sorted) < len(steps):
            available = [s
                         for s in steps
                         if s not in steps_sorted and
                         (s._prev_step is None or
                          s._prev_step.__get__(self, self.__class__) in steps_sorted)]
            assert len(available) == 1
            steps_sorted.append(available[0])
        return steps_sorted

    def execute(self):
        self.init_results()
        self._execute()

    def _execute(self, step_ind=0, prev_arguments={}, prev_results={}):
        step = self.steps[step_ind]

        pb = ProgressBar(step._args_prod_values,
                         title=step.__name__.replace('_', ' ').capitalize(),
                         key=id(step))
        for values in pb:
            pb.set_extra_text('Params: ' + '; '.join(['%s: %s' % (k, v)
                                                      for k, v in zip(step._args.names, values)]))

            cur_kwargs = dict()
            cur_kwargs.update(zip(step._args.names, values))
            cur_kwargs.update({k: prev_results[k]
                               for k in step._args_passable_names})

            cur_res = step(**cur_kwargs)
            assert set(cur_res.keys()) == set(step._results.keys()), 'Incorrect results specified'

            cur_arguments = prev_arguments.copy()
            cur_arguments.update(zip(step._args.names, values))

            self.add_result(step_ind, cur_arguments, cur_res)
            if step_ind < len(self.steps) - 1:
                cur_results = prev_results.copy()
                cur_results.update(cur_res)

                self._execute(step_ind + 1,
                              prev_arguments=cur_arguments,
                              prev_results=cur_results)

    def init_results(self):
        raise NotImplementedError

    def add_result(self, step_ind, args, result):
        raise NotImplementedError

