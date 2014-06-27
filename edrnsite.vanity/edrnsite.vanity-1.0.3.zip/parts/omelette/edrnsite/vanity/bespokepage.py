# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Bespoke page.'''

from Acquisition import aq_inner
from edrnsite.vanity import MESSAGE_FACTORY as _
from five import grok
from plone.directives import dexterity
from plone.directives import form
from plone.namedfile.field import NamedImage
from zope import schema
from zope.component import getMultiAdapter
import re

_mboxRE = re.compile(r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$', re.IGNORECASE)
def _checkEmail(value):
    '''Check if the given value is an email address.'''
    return _mboxRE.match(value) is not None


class IBespokePage(form.Schema):
    '''A bespoke page.'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u"Enter your name, as you'd like it to appear."),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'Type up a short summary. You might include research interests, personal background, funny quirks, etc.'),
        required=False,
    )
    showMbox = schema.Bool(
        title=_(u'Show My Email'),
        description=_(u'Check the box if you want your email address displayed publicly. Leave it unchecked to keep it hidden.'),
        required=False,
    )
    mbox = schema.TextLine(
        title=_(u'Email Address'),
        description=_(u"Address of your email inbox. We won't share it! But check the box above if want it shown to visitors."),
        required=True,
        constraint=_checkEmail
    )
    phone = schema.TextLine(
        title=_(u'Telephone Number'),
        description=_(u"Your phone number. (This will be visible to anyone, so clear it out if you want more privacy.)"),
        required=False,
    )
    edrnTitle = schema.TextLine(
        title=_(u'EDRN Title'),
        description=_(u'Title or honorific given by the Early Detection Research Network'),
        required=False,
    )
    specialty = schema.TextLine(
        title=_(u'Speciality'),
        description=_(u'Your area of specialization.'),
        required=False,
    )
    photograph = NamedImage(
        title=_(u'Photograph'),
        description=_(u'Upload a photograph of yourself. Please, keep it tasteful.'),
        required=False,
    )
    dexterity.write_permission(siteName='cmf.ManagePortal')
    siteName = schema.TextLine(
        title=_(u'Site Name'),
        description=_(u'Name of the site where you work.'),
        required=False,
    )
    dexterity.write_permission(memberType='cmf.ManagePortal')
    memberType = schema.TextLine(
        title=_(u'Member Type'),
        description=_(u'What particular kind of member site this.'),
        required=False,
    )
    dexterity.write_permission(piUID='cmf.ManagePortal')
    piUID = schema.TextLine(
        title=_(u'PI UID'),
        description=_(u'Unique identifier of the principal investigator of the site where this person works.'),
        required=False,
    )
    
    

class View(grok.View):
    '''View for a bespoke page.'''
    grok.context(IBespokePage)
    grok.require('zope2.View')
    def isMine(self):
        context = aq_inner(self.context)
        state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        if state.anonymous():
            return False
        userID = state.member().getUser().getId()
        pageOwnerID = context.getOwner().getId()
        if userID != pageOwnerID:
            return False
        contextState = getMultiAdapter((context, self.request), name=u'plone_context_state')
        return contextState.is_editable()
    def _getWorkflowState(self):
        context = aq_inner(self.context)
        contextState = getMultiAdapter((context, self.request), name=u'plone_context_state')
        return contextState.workflow_state()
    def isPublic(self):
        return self._getWorkflowState() in ('public', 'visible')
    def isPrivate(self):
        return self._getWorkflowState() == 'private'
    def _getCanonicalURL(self):
        context = aq_inner(self.context)
        contextState = getMultiAdapter((context, self.request), name=u'plone_context_state')
        return contextState.canonical_object_url()
    def editURL(self):
        return self._getCanonicalURL() + '/edit'
    def publishURL(self):
        return self._getCanonicalURL() + '/content_status_modify?workflow_action=show'
    def privateURL(self):
        return self._getCanonicalURL() + '/content_status_modify?workflow_action=hide'
