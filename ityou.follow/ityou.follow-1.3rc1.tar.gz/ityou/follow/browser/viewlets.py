# -*- coding:utf-8 -*-
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.viewlet.interfaces import IViewlet

from plone import api

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from ..dbapi import DBApi
from .. import _

dbapi = DBApi()

class FollowViewlet(BrowserView):
    """Viewlet used to display the buttons
    """
    implements(IViewlet)
    render = ViewPageTemplateFile("templates/follow.pt")

    def __init__(self, context, request, view=None, manager=None):
        super(FollowViewlet, self).__init__(context, request)
        self.context = context

    def isAuthenticatedMember(self):
        """ Checks if the viewer is authenticated.
        """
        if api.user.is_anonymous():
            return False
        else:
            return True
    
    def isFollowing(self):
        """ Checks if the authenticated member is following the author
        """
        mt = getToolByName(self.context, "portal_membership")
        auth_member = mt.getAuthenticatedMember()
        auth_member_id = auth_member.getId()
        author = self.context.Creator()

        return dbapi.isFollowing(auth_member_id, author)
    
    def author(self):
        """ Returns author of the current object
        """
        return self.context.Creator()

    def authorname(self):
        """ Returns authorname of the current object
        """
        mt = getToolByName(self.context, "portal_membership")
        creator = mt.getMemberById(self.context.Creator())        
        if creator:
            authorname = creator.getProperty("fullname") or creator.getId()
        else:
            authorname = ''
        return authorname

    def isMe(self):
        """ Returns if the creator is the authenticatedMember
        """
        mt = getToolByName(self.context, "portal_membership")
        return mt.getAuthenticatedMember().getId() == self.context.Creator()

    def followText(self):
        """ Returns follow text to show in template
        """
        msgid = _(u"follow_btn" , default=u"Follow ${authorname}", mapping={ u"authorname" : self.authorname().decode("utf-8")})
        return self.context.translate(msgid)

    def unfollowText(self):
        """ Returns Unfollow text to show in template
        """
        msgid = _(u"unfollow_btn" , default=u"Unfollow ${authorname}", mapping={ u"authorname" : self.authorname().decode("utf-8")})
        return self.context.translate(msgid)
