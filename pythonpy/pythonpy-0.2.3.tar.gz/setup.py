from distutils.core import setup
import os

setup(
    name='pythonpy',
    version='0.2.3',
    description='Take advantage of your python skills from the command line',
    scripts=[os.path.join('bin', 'pythonpy')],
    license='MIT',
    url='https://github.com/Russell91/pythonpy',
    long_description='',
)
