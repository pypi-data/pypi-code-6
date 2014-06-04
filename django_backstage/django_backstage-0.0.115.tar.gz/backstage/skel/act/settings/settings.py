### DO NOT EDIT THIS FILE ###
### store site specific settings 
### in local_settings.py
#############################
import os

sys.path.append('/data/www/duck/sites')

PROJECT_NAME = 'duck'
PROJECT_PATH = '/data/www'
LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_PATH = os.path.dirname(LOCAL_PATH)

PROJECT_PATH in sys.path or sys.path.insert(0,PROJECT_PATH)
LOCAL_PATH   in sys.path or sys.path.insert(0,LOCAL_PATH)
PARENT_PATH  in sys.path or sys.path.insert(1,PARENT_PATH)

SITE_NAME = os.path.basename(LOCAL_PATH)
ROOT_URLCONF = SITE_NAME + '.urls'

#IMPORT VENUE SETTINGS
s='from %s import *' % (PROJECT_NAME + '.settings')
exec(s)


TEMPLATE_DIRS = [os.path.join(LOCAL_PATH,'templates'),] + TEMPLATE_DIRS

# add the site's site folder to installed apps:
# bump the site to the top of installed apps
if not '%s.site' % (SITE_NAME) in INSTALLED_APPS:
    #exec("INSTALLED_APPS.append('" + SITE_NAME + ".site')")
    INSTALLED_APPS.insert(0,SITE_NAME)

# set the MEDIA_URL by extending the value from static_settings
MEDIA_URL = MEDIA_URL + 'site/%s/' % SITE_NAME
# set the MEDIA_ROOT as an absolute file path
MEDIA_ROOT = MEDIA_ROOT_BASE + '%s/' % SITE_NAME

#set a prefix for the cache
if len(CACHES) > 0:
    CACHES['default']['KEY_PREFIX'] = SITE_NAME

# site settings are generated and shouldn't be edited.
from site_settings import *

# local settings are unique within each site and are manually edited
# they are imported after site_settings and over-ride those
try: 
    from skel.act.settingfs.local_settings import *
except:
    pass #file not found

# import the theme settings, and add it to the TEMPLATE_DIRS                                           # it should end up second in the list behind the site templates 
try:
    from skel.act.settingfs.theme_settings import MAINTHEME
    if MAINTHEME is None:
        MAINTHEME = 'default'
    TEMPLATE_DIRS.insert(1,(os.path.join(PROJECT_ROOT,'project/themes',MAINTHEME,'templates')))
except:
    raise

# add any site apps to the installed apps, if they exist
if os.path.exists(os.path.join(LOCAL_PATH,'site_apps.py')):
    from site_apps import SITE_APPS
    for app in SITE_APPS:
        if not app in INSTALLED_APPS:
            INSTALLED_APPS.append(app)

# stuff below depends on the local settings

#add the site database to the databases dict
if SITE_DB <> 'None' and SITE_DB is not None:
    DATABASES['site'] = {
         'NAME':SITE_DB,'ENGINE':DBENGINE,'HOST':DBHOST,
         'PORT':DBPORT,'USER':DBUSER,'PASSWORD':DBPASS}

