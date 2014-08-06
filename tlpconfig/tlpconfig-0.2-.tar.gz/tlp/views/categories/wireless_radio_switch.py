from .category import Category


class WirelessRadioSwitch(Category):
    CATEGORY='WIRELESS_RADIO_SWITCH'

    def __init__(self, loader, configuration_groups):
        Category.__init__(self, self.CATEGORY, loader)
        self.set_groups(configuration_groups)
