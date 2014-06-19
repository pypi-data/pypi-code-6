from distutils.core import setup
import os

try:
     with open('/etc/bash_completion.d/pycompletion_test.sh', 'w') as eo:
         eo.write('test3')
     data_files = [('/etc/bash_completion.d', ['extras/pycompletion.sh']),]
except:
     print 'User does not have write access to /etc completion will not work'
     data_files = [('bash_completion.d', ['extras/pycompletion.sh']),]

setup(
    name='pythonpy',
    version='0.2.6dev4',
    description='Take advantage of your python skills from the command line',
    scripts=['py', 'extras/pycompleter', 'extras/wpy'],
    data_files=data_files,
    license='MIT',
    url='https://github.com/Russell91/pythonpy',
    long_description='',
)
