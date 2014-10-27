import logging

class LoggerFactory:

	@staticmethod
	def createLogger(name, verbose):
		logging.basicConfig(format='%(asctime)s %(name)s:%(lineno)s %(message)s', level=LoggerFactory._createLevel_(verbose))
		return logging.getLogger(name)
		
	@staticmethod
	def _createLevel_(verbose):
		level = logging.WARNING
		if verbose:
			level = logging.DEBUG

		return level