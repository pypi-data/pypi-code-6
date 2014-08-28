import RPIO


class WrongGPIOConfiguration(Exception):
    pass

USED_GPIO_LIST = RPIO.GPIO_LIST_R2 if RPIO.RPI_REVISION == 2 else RPIO.GPIO_LIST_R1