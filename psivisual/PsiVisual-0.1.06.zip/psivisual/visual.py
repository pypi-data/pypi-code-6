
from __future__ import print_function, division, absolute_import
import pyximport
import sys
setup_args = {}
if sys.platform == 'win32':
    setup_args = {'options':{'build_ext':{'compiler':'mingw32'}}}
pyximport.install(setup_args=setup_args);

from IPython.display import display, HTML
import os
import IPython.html.nbextensions

display(HTML("""<div id="scene"><div id="glowscript" class="glowscript"></div></div>"""))

package_dir = os.path.dirname(__file__)
IPython.html.nbextensions.install_nbextension(files=[package_dir+"/data/glow.1.0.min.js",package_dir+"/data/glowcomm.js"],overwrite=True,verbose=0)

from psivisual.psiobjects import *
