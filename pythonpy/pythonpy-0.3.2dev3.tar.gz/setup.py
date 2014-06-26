from distutils.core import setup
import os

if os.geteuid() == 0:
     data_files = [('/etc/bash_completion.d', ['extras/pycompletion.sh']),]
else:
     print(
'''******************************************************************************
PERMISSION DENIED: User does not have write access to /etc.
To add completion manually, run
    source bash_completion.d/pycompletion.sh
from the install directory.
*****************************************************************************''')
     data_files = [('bash_completion.d', ['extras/pycompletion.sh']),]

setup(
    name='pythonpy',
    version='0.3.2dev3',
    description='python -c, with tab completion and shorthand',
    scripts=['py', 'extras/py3', 'extras/pycompleter'],
    data_files=data_files,
    license='MIT',
    url='https://github.com/Russell91/pythonpy',
    long_description='',
)
