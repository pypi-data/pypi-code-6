import re
import RPIO
from hautomation_gpio import USED_GPIO_LIST


def is_input(address):
    return RPIO.gpio_function(address) == RPIO.IN


def is_output(address):
    return RPIO.gpio_function(address) == RPIO.OUT


def validate_address(address):
    if address not in USED_GPIO_LIST:
        raise ValueError("Unsupported address: %s for GPIO \
            driver with Hardware revision: %s" % (
                address,
                RPIO.RPI_REVISION,
            ))
    return True
