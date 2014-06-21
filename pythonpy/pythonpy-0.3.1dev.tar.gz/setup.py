from distutils.core import setup
import os

if os.geteuid() == 0:
     data_files = [('/etc/bash_completion.d', ['extras/pycompletion.sh']),]
else:
     print('User does not have write access to /etc completion will not work')
     data_files = [('bash_completion.d', ['extras/pycompletion.sh']),]

setup(
    name='pythonpy',
    version='0.3.1dev',
    description='Take advantage of your python skills from the command line',
    scripts=['py', 'extras/py3', 'extras/pycompleter'],
    data_files=data_files,
    license='MIT',
    url='https://github.com/Russell91/pythonpy',
    long_description='',
)
