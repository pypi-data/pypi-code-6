import re
import RPIO
from hautomation_gpio import USED_GPIO_LIST


def validate_address(address):
    if int(address) not in USED_GPIO_LIST:
        raise ValueError("Unsupported address: %s for GPIO \
            driver with Hardware revision: %s" % (
                address,
                RPIO.RPI_REVISION,
            ))
    return True
