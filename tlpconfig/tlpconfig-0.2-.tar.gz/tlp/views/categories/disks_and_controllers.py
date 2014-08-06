from .category import Category


class DisksAndControllers(Category):
    CATEGORY='DISKS_AND_CONTROLLERS'

    def __init__(self, loader, configuration_groups):
        Category.__init__(self, self.CATEGORY, loader)
        self.set_groups(configuration_groups)
