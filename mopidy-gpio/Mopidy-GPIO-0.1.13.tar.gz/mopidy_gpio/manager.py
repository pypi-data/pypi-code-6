import logging

import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)
#	GPIO.RISING, GPIO.FALLING or GPIO.BOTH.

class GPIOManager():
    def __init__(self, backend, pins):
		self.backend = backend
		
		# GPIO Mode
        GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		GPIO.setup(17, GPIO.IN)
		GPIO.add_event_detect(17, GPIO.FALLING, callback=callback_mute)
		
	def callback_mute(channel):
		logger.info('GPIO: [GPIOManager] callback_mute trigged')
		if ( GPIO.input(channel) == False ):
			self.backend.mute()