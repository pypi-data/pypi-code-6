import sys
import os
print __file__
syspath = sys.path
p = os.path.dirname(os.path.abspath(__file__)) # settings
p2,n2 = os.path.split(p) # act name  /tmp/asdf/acts/act0 settings
p3,n3 = os.path.split(p2) # acts     /tmp/asdf/acts act0
p4 = os.path.dirname(p3) # venue name
p5,n5 = os.path.split(p4) # venue base
sys.path.insert(0,p3)
sys.path.insert(1,p5)
exec('from %s.settings import *' % n5) 

from theme_settings import *
from db_settings import DATABASES
from act_settings import *

INSTALLED_APPS.insert(0, n3)

TEMPLATE_DIRS.insert(0, n3 + '/templates')

ROOT_URLCONF = '%s.urls' % (n3)
