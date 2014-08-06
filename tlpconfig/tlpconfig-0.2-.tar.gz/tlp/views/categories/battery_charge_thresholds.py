from .category import Category


class BatteryChargeThresholds(Category):
    CATEGORY='BATTERY_CHARGE_THRESHOLDS'

    def __init__(self, loader, configuration_groups):
        Category.__init__(self, self.CATEGORY, loader)
        self.set_groups(configuration_groups)
