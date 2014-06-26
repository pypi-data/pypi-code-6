
import os.path as p
import logging

FORMAT = '%(asctime)-15s %(levelname)-10s %(message)s'

logging.basicConfig(level=logging.INFO, format = FORMAT)

class ConfigDict:
	'''The recursive class for building and representing objects with.'''
	def __init__(self, obj):
		for k, v in obj.iteritems():
			if isinstance(v, dict):
				setattr(self, k, Struct(v))
			else:
				setattr(self, k, v)
	def __getitem__(self, val):
		return self.__dict__[val]
	def __repr__(self):
		return '{%s}' % str(', '.join('%s : %s' % (k, repr(v)) for (k, v) in self.__dict__.iteritems()))

__dirname = p.dirname(p.abspath(__file__))

paths = ConfigDict({
	'python': __dirname,
	'resources': p.join(__dirname, 'resources')
})

PING_FREQUENCY = 500

def get_resource(*args):
	sub = p.join(*args)
	return p.join(paths.resources, sub)

