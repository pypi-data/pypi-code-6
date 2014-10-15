from Products.CMFPlone.utils import getToolByName
from plone.app.upgrade.utils import installOrReinstallProduct
from plone.app.upgrade.utils import loadMigrationProfile
from zope.component import getUtility
from Products.CMFCore.interfaces import IPropertiesTool


PROFILE_ID = 'profile-collective.superfish:default'


def _cookResources(portal):
    jstool = getToolByName(portal, 'portal_javascripts')
    jstool.cookResources()
    csstool = getToolByName(portal, 'portal_css')
    csstool.cookResources() 

    
def to_2(context):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    _cookResources(portal)

