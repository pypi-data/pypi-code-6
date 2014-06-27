# encoding: utf-8
# Copyright 2013 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getMultiAdapter
from five import grok
from Acquisition import aq_inner
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
from edrnsite.vanity import VANITY_UPDATE_KEY
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class _VanityView(grok.View):
    '''Common view for vanity welcomes, nags, etc.'''
    grok.baseclass()
    grok.context(ISiteRoot)
    def update(self):
        context = aq_inner(self.context)
        self.plone_portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        smd = getToolByName(context, 'session_data_manager')
        session = smd.getSessionData(create=False)
        if session and session.has_key(VANITY_UPDATE_KEY):
            del session[VANITY_UPDATE_KEY]
    def haveUser(self):
        return not self.plone_portal_state.anonymous()
    def userName(self):
        return self.plone_portal_state.member().getProperty('fullname')
    def vanityPageURL(self):
        normalizer = getUtility(IIDNormalizer)
        return u'%s/member-pages/%s' % (
            self.plone_portal_state.portal_url(),
            normalizer.normalize(self.plone_portal_state.member().getUserName())
        )


class VanityWelcomeView(_VanityView):
    '''View to welcome users to their new vanity pages.'''
    
class VanityNagView(_VanityView):
    '''View to remind users to visit their vanity pages.'''

