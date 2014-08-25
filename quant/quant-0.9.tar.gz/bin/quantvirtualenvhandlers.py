import os
activateThisPath = os.path.join(os.path.dirname(__file__), 'activate_this.py')
execfile(activateThisPath, dict(__file__=activateThisPath))

# Quant Web UI Mod_python handler (for use with virtualenv).
from quant.handlers.modpython import handler as djangohandler

