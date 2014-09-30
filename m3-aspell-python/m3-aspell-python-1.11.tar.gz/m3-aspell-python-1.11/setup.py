from distutils.core import setup, Extension

module1 = Extension('aspell', libraries = ['aspell'], library_dirs = ['/usr/local/lib/'], sources = ['aspell.c'])

setup (name = 'm3-aspell-python',
	version = '1.11',
	ext_modules = [module1])
