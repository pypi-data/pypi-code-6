from setuptools import setup, find_packages  # Always prefer setuptools over distutils

setup(
	name='boopyboop',
	version="0.0.1",
	description="Turn long numbers in whatever format to human-readable long series of words",
	url="https://github.com/howonlee/boopyboop",
	author="Howon Lee",
	author_email="howon@howonlee.com",
	license="MIT",
	classifiers=[
		'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
		],
	install_requires=['python-baseconv']
	)

