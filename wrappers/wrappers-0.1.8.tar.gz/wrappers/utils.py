# logger
import os, logging, time
logging.basicConfig()

DIGESTLEN = 5

class register:
	handlers = dict()
	def __init__(self, action):
		self._action = action
	def __call__(self, func):
		register.handlers[self._action] = func

def getLogger(name):
	logger = logging.getLogger(name)
	if "LOG_LEVEL" in os.environ:
		s = os.getenv('LOG_LEVEL')
		logger.setLevel(int(s) if s.isdigit() else getattr(logging, s))
	return logger

# generate sha1 digest
from hashlib import sha1, sha256, sha512
def digest(s):
	return sha512(s).digest()[:DIGESTLEN]

class Clock:
	def __init__(self):
		self._start = time.time()
	def elapsed(self):
		return time.time() - self._start
