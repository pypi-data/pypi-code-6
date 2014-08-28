import logging
from django.conf import settings
#logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.INFO)


class Logger():

	@staticmethod
	def getLogger():
		#Simple wrapper. Ensures logging is always correctly configured (logging.basicConfig is executed)
		logger = logging.getLogger("thermostat")
        logger.setLevel(settings.LOG_LEVEL)
        return logger
