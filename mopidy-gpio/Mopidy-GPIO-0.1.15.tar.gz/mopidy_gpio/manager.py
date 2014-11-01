import logging

import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)
#	GPIO.RISING, GPIO.FALLING or GPIO.BOTH.

class GPIOManager():
    def __init__(self, backend, pins):
        logger.info('GPIO: [GPIOManager]')
        self.backend = backend

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # RadioStation 1
        GPIO.setup(pins['pin_button_radio_1'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pins['pin_button_radio_1'], GPIO.RISING, callback=self.mute_callback)
        # RadioStation 2
        GPIO.setup(pins['pin_button_radio_2'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pins['pin_button_radio_2'], GPIO.RISING, callback=self.mute_callback)
        # RadioStation 3
        GPIO.setup(pins['pin_button_radio_3'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pins['pin_button_radio_3'], GPIO.RISING, callback=self.mute_callback)
        # RadioStation 4
        GPIO.setup(pins['pin_button_radio_4'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pins['pin_button_radio_4'], GPIO.RISING, callback=self.mute_callback)
        # RadioStation 5
        GPIO.setup(pins['pin_button_radio_5'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pins['pin_button_radio_5'], GPIO.RISING, callback=self.mute_callback)

        logger.info('GPIO: [GPIOManager] DONE')

    def mute_callback(self, channel):
        self.backend.mute()
        logger.info('GPIO: [GPIOManager] MUTE')

    def on_stop(self):
        GPIO.cleanup()
        logger.info('GPIO: [GPIOManager] Cleaning up')