import os, logging
logging.basicConfig()

__doc__ = """
reads LOG_LEVEL environment variable to set the log level for the logging module
e.g. LOG_LEVEL=10 python somescript.py
e.g. LOG_LEVEL=30 python somescript.py
e.g. LOG_LEVEL=DEBUG python somescript.py
e.g. LOG_LEVEL=WARNING python somescript.py
"""

def getLogger(name):
	logger = logging.getLogger(name)
	if "LOG_LEVEL" in os.environ:
		s = os.getenv('LOG_LEVEL')
		logger.setLevel(int(s) if s.isdigit() else getattr(logging, s))
	return logger
