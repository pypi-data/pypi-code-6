# -*- coding: utf-8 -*-
import logging
from zope.component.hooks import getSite
from zope.i18nmessageid import MessageFactory
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
_ = MessageFactory('ityou.imessage')


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

def getNotifyDBApi():
    """Loads Notify DBApi Function
    Returns False if the product is not installed
    """
    dbapi_notify = False
    
    qui = getSite().portal_url.getPortalObject().portal_quickinstaller
    installed_products = qui.listInstalledProducts()
    
    for product in installed_products:
        if product["id"] == "ityou.notify" and product["status"] == "installed":
            try:
                from ityou.notify.dbapi import DBApi
                from ityou.notify.interfaces import INotifySettings
                if getUtility(IRegistry).forInterface(INotifySettings).imessage_notifications_active:
                    dbapi_notify = DBApi()
                else:
                    logging.info("ityou.imessage says: ITYOU Notify App is deactivated - No emails will be send")
            except:
                logging.info("ityou.imessage says: Could not load ITYOU Notify App - No emails will be send")
            
    return dbapi_notify

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
