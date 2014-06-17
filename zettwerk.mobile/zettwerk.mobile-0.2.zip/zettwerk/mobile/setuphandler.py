from plone.registry.interfaces import IRegistry
from zope.component import getUtility


def import_various(context):
    """ set zettwerk.mobile as default theme for zettwerk.mobiletheming """
    if context.readDataFile('zettwerk.mobile-various.txt') is None:
        return

    registry = getUtility(IRegistry)
    registry['zettwerk.mobiletheming.interfaces.IMobileThemingSettings' \
             '.themename'] = u'zettwerk.mobile'
