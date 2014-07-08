# -*- coding: utf-8 -*-
from zope.component.hooks import getSite
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("ityou.extuserprofile")

# Install/Uninstall the default memberfolder view
INDEX     = "index_html"
INDEX_OFF = "index_html.DO_NOT_DELETE"

INSTANCE_PATH   = '/'.join(INSTANCE_HOME.split('/')[:-2])

try:
    from ityou.astream.browser.activities import ActivityUtils
    activity_utils = ActivityUtils()
except:
    activity_utils = False


def getIMessage():
    dbapi_imessage = False
    plone = getSite()
    qui = plone.portal_url.getPortalObject().portal_quickinstaller
    installed_products = qui.listInstalledProducts()
    for product in installed_products:
        if product["id"] == "ityou.imessage" and product["status"] == "installed":
            try:
                from ityou.imessage.dbapi import DBApi as DBApi_imessage
                dbapi_imessage = DBApi_imessage()
            except:
                dbapi_imessage = False
    return dbapi_imessage

def getAstream():
    dbapi_astream = False
    plone = getSite()
    qui = plone.portal_url.getPortalObject().portal_quickinstaller
    installed_products = qui.listInstalledProducts()
    for product in installed_products:
        if product["id"] == "ityou.astream" and product["status"] == "installed":
            try:
                from ityou.astream.dbapi import DBApi as DBApi_astream
                dbapi_astream = DBApi_astream()
            except:
                dbapi_astream = False
    return dbapi_astream



def initialize(context):
    """Initializer called when used as a Zope 2 product."""
