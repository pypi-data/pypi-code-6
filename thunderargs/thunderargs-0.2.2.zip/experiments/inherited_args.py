__author__ = 'thunder'

from thunderargs import Arg

from thunderargs.validfarm import val_gt, val_lt, len_gt, len_lt

class IntArg(Arg):

    def __init__(self, max_val=None, min_val=None, **kwargs):
        kwargs['p_type'] = int
        if not 'validators' in kwargs or kwargs['validators'] is None:
            kwargs['validators'] = []

        if min_val is not None:
            if not isinstance(min_val, int):
                raise TypeError("Minimal value must be int")

            kwargs['validators'].append(val_gt(min_val-1))

        if max_val is not None:
            if not isinstance(max_val, int):
                raise TypeError("Maximal value must be int")

            kwargs['validators'].append(val_lt(max_val+1))

        if min_val is not None and max_val is not None:
            if max_val < min_val:
                raise ValueError("max_val is greater than min_val")

        super().__init__(**kwargs)




class ListArg(Arg):

    def __init__(self, **kwargs):
        kwargs['multiple'] = True
        super().__init__(**kwargs)