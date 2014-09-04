from distutils.core import setup

setup(
	name='px',
	version='0.1.0',
	author='6px',
	author_email='ops@6px.io',
	packages=['_6px'],
    url='https://github.com/6px-io/6px-python',
	license='MIT',
	description='Python module for 6px',
	install_requires=['websocket-client']
)
