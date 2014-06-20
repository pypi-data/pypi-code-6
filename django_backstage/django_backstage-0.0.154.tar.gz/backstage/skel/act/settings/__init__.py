import sys
import os
syspath = sys.path
p = os.path.dirname(os.path.abspath(__file__)) # settings
ACT_HOME, n2 = os.path.split(p) # act name  /tmp/asdf/acts/act0 settings
ACTS_DIR, ACT_NAME = os.path.split(ACT_HOME) # acts     /tmp/asdf/acts act0
VENUE_NAME = os.path.dirname(ACTS_DIR) # venue name
p5, n5 = os.path.split(VENUE_NAME) # venue base
sys.path.insert(0,ACTS_DIR)
sys.path.insert(1,p5)
exec('from %s.settings import *' % n5) 

from theme_settings import *


from db_settings import DATABASES
DATABASES['default']['NAME'] = 'backstage_%s_%s' % (VENUE_NAME, ACT_NAME)

from act_settings import *

INSTALLED_APPS.insert(0, ACT_NAME)

TEMPLATE_DIRS.insert(0, ACT_NAME + '/templates')

ROOT_URLCONF = '%s.urls' % (ACT_NAME)

STATIC_ROOT = os.path.join(ACT_HOME,'cstatic/')
STATIC_URL = '/static/'

INSTALLED_APPS += ACT_APPS

del p, p5, n5
