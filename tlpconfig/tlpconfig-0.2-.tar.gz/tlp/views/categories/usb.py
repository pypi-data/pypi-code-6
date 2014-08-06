from .category import Category


class Usb(Category):
    CATEGORY='USB'

    def __init__(self, loader, configuration_groups):
        Category.__init__(self, self.CATEGORY, loader)
        self.set_groups(configuration_groups)
