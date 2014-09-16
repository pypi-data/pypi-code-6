# -*- coding: utf-8 -*-
import logging
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from ityou.esi.theme.interfaces import IESIThemeSettings
from . import _

# --- psql -----------------------------------------------------
from ityou.esi.theme import PSQL_URI
# --- /psql -----------------------------------------------------

DB_LOCATION = '/'.join(INSTANCE_HOME.split('/')[:-2]) + "/var/sqlite3"
DB          = "sqlite:///"+ DB_LOCATION +  "/ityou.extuserprofile.db"
TABLE       = 'extuserprofile'
TIMEOUT     = 600

###USER_ID_BLACKLIST = ['admin']     

salutations = SimpleVocabulary([
    SimpleTerm(value=u'Mr', title=_(u'Mr')),
    SimpleTerm(value=u'Mrs', title=_(u'Mrs'))
    ])

# Image tag for portraits
IMG_TAG = '<img class="img-tile img-thumbnail" src="%s" title="%s"/>'

# Structure for datatable user list 
LAST_LOGIN_STRING = '<span class="hiddenStructure">%s</span><span>%s</span>'

# Default date that plone sends if a user has not been logged in yet
DEFAULT_START_DATE =  "2000/01/01 00:00:00 GMT+1"

# Properties in fullname
FULLNAME_PROPERTIES = ["acadtitle", "firstname", "lastname"]

# brauchen den Benutzer um Accounts zu löschen!
ONKONNEKT_ADMIN = 'onkonnekt_admin'
ONKONNEKT_ADMIN_PWD = 'on12ad90'
