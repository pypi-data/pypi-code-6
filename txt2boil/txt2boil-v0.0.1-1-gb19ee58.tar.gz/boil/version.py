"""The version module for this package.

Whenever this module is imported, it will always attempt to update its
version string by fetching a new one from the VCS.  If that fails then
it retains the one that's already saved to it.

Currently, only git is a supported VCS.

"""

import re
import subprocess
import sys

try:
    version = subprocess.check_output(['git', 'describe'])
    version = version.split()[0]
except OSError, CalledProcessError:
    version = 'v0.0.1-1-gb19ee58'
    
filename = sys.modules[__name__].__file__
with open(filename) as f:
    code = f.read()
code = re.sub(r"^(\s*version = )'.*$", '\g<1>' + repr(version), code, 1, re.M)
with open(filename, 'w') as f:
    f.write(code)
