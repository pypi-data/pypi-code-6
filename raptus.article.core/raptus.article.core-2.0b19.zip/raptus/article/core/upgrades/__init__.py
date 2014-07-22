from Products.CMFPlone.utils import getToolByName
from plone.app.upgrade.utils import installOrReinstallProduct
from plone.app.upgrade.utils import loadMigrationProfile
from zope.component import getUtility
from Products.CMFCore.interfaces import IPropertiesTool


PROFILE_ID = 'profile-raptus.article.core:default'


def _cookResources(context):
    jstool = getToolByName(context, 'portal_javascripts')
    jstool.cookResources()
    csstool = getToolByName(context, 'portal_css')
    csstool.cookResources() 

    
def to_11(context):
    
    portal = getToolByName(context, 'portal_url').getPortalObject()
    #installOrReinstallProduct(portal, 'raptus.article.listings')
    _cookResources(portal)

 

    
     
