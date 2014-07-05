import sys


def generate(path):
	def fn(instance, filename):
		import os.path
		from uuid import uuid4
		ext = filename.split('.')[-1]
		filename = '{}.{}'.format(uuid4().hex, ext)
		return os.path.join(path, filename)
	return fn

sys.modules[__name__] = generate

