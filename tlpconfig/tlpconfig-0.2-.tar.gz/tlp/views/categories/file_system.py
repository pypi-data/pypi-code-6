from .category import Category


class FileSystem(Category):
    CATEGORY='FILE_SYSTEM'

    def __init__(self, loader, configuration_groups):
        Category.__init__(self, self.CATEGORY, loader)
        self.set_groups(configuration_groups)
