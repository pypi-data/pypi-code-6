from .category import Category


class RuntimePowerManagement(Category):
    CATEGORY='RUNTIME_POWER_MANAGEMENT'

    def __init__(self, loader, configuration_groups):
        Category.__init__(self, self.CATEGORY, loader)
        self.set_groups(configuration_groups)
