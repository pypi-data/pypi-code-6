from ...models import (BooleanParameter, ListParameter,
                       NumericParameter, TextParameter)
from .default_binders import (BooleanParameterBinder, ListParameterBinder,
                              NumericParameterBinder, TextParameterBinder )


class ParameterBinderSelector:
    def __init__(self):
        self.binders = {BooleanParameter: BooleanParameterBinder,
                        ListParameter: ListParameterBinder,
                        NumericParameter: NumericParameterBinder,
                        TextParameter: TextParameterBinder}

    def get_from(self, parameter):
        binder = self.binders[type(parameter)]
        return binder(parameter)

    def set_binder(self, parameter_type, binder_type):
        self.binders[parameter_type] = binder_type
