from utils import *
import RPIO
from hautomation_gpio import WrongGPIOConfiguration, USED_GPIO_LIST


def set_to_output(address):
    validate_address(address)
    RPIO.setup(address, RPIO.OUT)


def pl_switch(address, value):
    if value not in ["on", "off"]:
        raise ValueError("Switch value must be 'on' or 'off'")

    validate_address(address)

    if not is_output(address):
        raise WrongGPIOConfiguration("GPIO%s is not OUTPUT configured" % address)

    RPIO.output(address, value == "on")


def pl_all_lights_on():
    for pin in USED_GPIO_LIST:
        try:
            pl_switch(pin, "on")
        except WrongGPIOConfiguration:
            continue


def pl_all_lights_off():
    for pin in USED_GPIO_LIST:
        try:
            pl_switch(pin, "off")
        except WrongGPIOConfiguration:
            continue

