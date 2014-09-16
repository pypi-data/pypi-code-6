# -*- coding: utf-8 -*-
## -----------------------------------------------------------------
## Copyright (C)2013 ITYOU - www.ityou.de
## -----------------------------------------------------------------
"""
This module initialize the product ityou.dragdrop
"""
from zope.component.hooks import getSite
from Globals import INSTANCE_HOME
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('ityou.dragdrop')


DB_LOCATION    = '/'.join(INSTANCE_HOME.split('/')[:-2]) + "/var/sqlite3"
DB_DRAGDROP    = "sqlite:///"+ DB_LOCATION +  "/ityou.follow.db"
TABLE_DRAGDROP = 'dragdrop'


# Name des Trash-Orders, der im Benutzerordner abgelegt wird
TRASH_FOLDER   =  "trash"

def isProductAvailable(product):
    """Check if a product is installed and return True, 
    else return False
    """
    qui = getSite().portal_url.getPortalObject().portal_quickinstaller
    installed_products = qui.listInstalledProducts()
    for prod in installed_products:
        if prod["id"] == product and prod["status"] == "installed":
            return True
    return False

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
