from setuptools import setup

setup(
	name='templetize',
    version = '2014.09.21',
    description='Templetize is a script to convert a file or a directory (recursively) to a template for codegen. It is bundled with a simple code generator module to expand these templates.',
    author='Nico Hoffmann',
    author_email='info@maxdoom.com',
	py_modules=['codegen'],
	scripts=['templetize.py'],
	install_requires=['jinja2'],
	license='BSD',
	keywords = "templating code generator",
)