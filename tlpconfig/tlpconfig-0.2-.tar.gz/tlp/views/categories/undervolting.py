from ..binders import FreeTextParameterBinder
from ...models import TextParameter
from .category import Category


class Undervolting(Category):
    CATEGORY='UNDERVOLTING'

    def __init__(self, loader, configuration_groups):
        Category.__init__(self, self.CATEGORY, loader)

        self.value_binders.set_binder(TextParameter, FreeTextParameterBinder)

        self.set_groups(configuration_groups)
