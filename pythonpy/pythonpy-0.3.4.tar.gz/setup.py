from distutils.core import setup
import os

if os.geteuid() == 0:
     data_files = [('/etc/bash_completion.d', ['extras/pycompletion.sh']),]
else:
     print(
'''**************************************************************************
___  ____ ____ _  _ _ ____ ____ _ ____ _  _    ___  ____ _  _ _ ____ ___ 
|__] |___ |__/ |\/| | [__  [__  | |  | |\ |    |  \ |___ |\ | | |___ |  \ 
|    |___ |  \ |  | | ___] ___] | |__| | \|    |__/ |___ | \| | |___ |__/
PERMISSION DENIED: Cannot copy pycompletion.sh to /etc/bash_completion.d
To configure tab completion without root, run
    source /path/to/install_directory/bash_completion.d/pycompletion.sh
**************************************************************************''')
     data_files = [('bash_completion.d', ['extras/pycompletion.sh']),]

setup(
    name='pythonpy',
    version='0.3.4',
    description='python -c, with tab completion and shorthand',
    scripts=['py', 'extras/py3', 'extras/pycompleter'],
    data_files=data_files,
    license='MIT',
    url='https://github.com/Russell91/pythonpy',
    long_description='',
)
