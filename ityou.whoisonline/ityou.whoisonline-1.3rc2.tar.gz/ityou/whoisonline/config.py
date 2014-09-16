# -*- coding: utf-8 -*-
from . import _

##DB_LOCATION     = '/'.join(INSTANCE_HOME.split('/')[:-2]) + "/var/sqlite3"
##DB              = "sqlite:///"+ DB_LOCATION +  "/ityou.whoisonline.db"
TABLE           = 'whoisonline'
DEBUG           = False
TIME_STRING     = _(u"%d.%m.%Y at %H:%M:%S")

# min value for ajax time period 
MIN_WHOISONLINE_DELAY = 4000

# ---- this users will not be considered
USER_ID_BLACKLIST = ['admin']

# --- WhoIsOnline -----------------------
WHO_IS_ONLINE_LISTING = '@@who-is-online'

# --- WhoAmI ----------------------------
WHO_IS_ONLINE_LISTING = '@@who-am-i'
#


# --- REDIS ------------------------
REDIS_SERVER = '127.0.0.1'
# --- works with Plone 4
ZOPE_INSTANCE = INSTANCE_HOME.split('/')[-4].replace('-','_').replace('.', '_')
WIO_USERS_KEY = ZOPE_INSTANCE + '_' + "whoisonline:users"

