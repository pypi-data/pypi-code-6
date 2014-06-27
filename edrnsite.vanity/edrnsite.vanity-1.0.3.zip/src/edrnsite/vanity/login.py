# encoding: utf-8
# Copyright 2013 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

# Caveman
from five import grok

# Users
from AccessControl import Unauthorized
from Products.PlonePAS.plugins.ufactory import PloneUser
from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent

# Vanity
from edrnsite.vanity import VANITY_UPDATE_KEY, BESPOKE_WELCOME, BESPOKE_OLD, NAG_LIMIT, vanityPagesEnabled

# Zope component arch
from zope.component.hooks import getSite
from zope.component import getUtility

# Utilities
from datetime import date, datetime
from DateTime import DateTime
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFCore.utils import getToolByName
import logging

_logger = logging.getLogger(__name__)

@grok.subscribe(IUserLoggedInEvent)
def checkVanityPage(event):
    '''Upon logging in, check to see if the user has a vanity page.  If not, make one.
    If so, see if the user has visited it recently.  If not, nag the user.
    '''
    if not vanityPagesEnabled(): return
    portal = getSite()

    # Now check the user
    user = event.object
    if not isinstance(user, PloneUser):
        # We make member pages only for Plone accounts. Zope admin & others: shoo.
        return

    # Find the user's page
    normalizer = getUtility(IIDNormalizer)
    catalog = getToolByName(portal, 'portal_catalog')
    results = catalog()

    memberPageID = normalizer.normalize(user.getUserId())
    # FIXME
    # try:
    #     memberFolder = portal.restrictedTraverse('member-pages')
    # except (KeyError, Unauthorized):
    #     # member-pages folder is either missing or private, so don't bother
    #     _logger.exception('No accessible member-pages folder in the portal; no bespoke pages')
    #     return
    normalizer = getUtility(IIDNormalizer)
    memberPageID = normalizer.normalize(user.getUserId())
    sdm = getToolByName(portal, 'session_data_manager')
    session = sdm.getSessionData(create=True)
    if not memberFolder.has_key(memberPageID):
        try:
            _logger.info("User %s doesn't have a bespoke page; creating one", memberPageID)
            memberPage = memberFolder[memberFolder.invokeFactory('edrnsite.vanity.bespokepage', memberPageID)]
            memberPage.title = unicode(user.getProperty('fullname', u'UNKNOWN')) # FIXME: Not i18n
            memberPage.reindexObject()
            session.set(VANITY_UPDATE_KEY, BESPOKE_WELCOME)
        except Unauthorized:
            _logger.exception("member-pages folder isn't writeable")
            return
    else:
        lastNotification = user.getProperty('vanityPageUpdateDate', None)
        if isinstance(lastNotification, DateTime):
            lastNotification = lastNotification.asdatetime()
        lastNotification = date(lastNotification.year, lastNotification.month, lastNotification.day)
        interval = date.today() - lastNotification
        if interval > NAG_LIMIT:
            _logger.info("User %s hasn't been nagged in a long time (%d days); nagging", memberPageID, interval.days)
            session.set(VANITY_UPDATE_KEY, BESPOKE_OLD)
        _logger.info('User logged in: %s, last notified %r', user.getId(), user.getProperty('vanityPageUpdateDate'))
    user.setProperties(vanityPageUpdateDate=datetime.now())
