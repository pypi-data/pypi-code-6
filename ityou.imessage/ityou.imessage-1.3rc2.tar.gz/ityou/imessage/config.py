# -*- coding: utf-8 -*-
import logging
#from ityou.mailer.interfaces import IMailerSettings

# --- sqlite -----------------------------------------------------
DB_LOCATION = '/'.join(INSTANCE_HOME.split('/')[:-2]) + "/var/sqlite3"
DB          = "sqlite:///"+ DB_LOCATION +  "/ityou.imessage.db"
# --- /sqlite -----------------------------------------------------

# --- psql -----------------------------------------------------
from ityou.esi.theme import PSQL_URI
# --- /psql -----------------------------------------------------

## --- works with Plone 4
#ZOPE_INSTANCE = INSTANCE_HOME.split('/')[-4].replace('-','_').replace('.', '_')

TABLE_MESSAGES          = 'messages'
TABLE_MESSAGE_GROUPS    = 'message_groups'
TABLE_MESSAGE_FLAGS     = 'message_flags'
# --- /psql -----------------------------------------------------



DEBUG       = False

TIMEOUT     = 600

MIN_IMESSAGE_DELAY = 4000

USER_ID_BLACKLIST = ['admin']
                
TIME_STRING = u"%d.%m.%Y um %H:%M:%S Uhr" 

# --- replace text -------------------------------------------------------------
IMESSAGE_REGEX = [
                  {"search": r"(http://[^ ]+|https://[^ ]+|www.[^ ]+|//[^ ])", "replace": r'<a target="_blank" href="\1">\1</a>'},
                  ]

