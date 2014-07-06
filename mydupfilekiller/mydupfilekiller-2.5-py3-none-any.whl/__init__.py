__author__ = "Wiadufa Chen <wiadufachen@gmail.com>"
__version__ = "2.5"
import pyximport
a, b = pyximport.install()
from mydupfilekiller.core import *
from mydupfilekiller.console import *
from mydupfilekiller.gui import *
from mydupfilekiller.exceptions import *
pyximport.uninstall(a, b)


