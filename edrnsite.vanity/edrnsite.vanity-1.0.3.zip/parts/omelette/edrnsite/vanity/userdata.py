# encoding: utf-8
# Copyright 2013 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

# i18n machinery
from edrnsite.vanity import MESSAGE_FACTORY as _

# User data schema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter

# Zope schema & component arch
from zope import schema
from zope.interface import implements

# Utils
from datetime import datetime, date
from DateTime import DateTime as oldDateTime


class IVainUserDataSchema(IUserDataSchema):
    '''Vain user data schema extends the Plone standard user data schema and adds fields for vanity.'''
    vanityPageUpdateDate = schema.Date(
        title=_(u'Vanity Page Update Date'),
        description=_(u"The date the user's vanity page was last updated; if unset, it means never updated."),
        required=False,
    )
    vanityPageLocation = schema.TextLine(
        title=_(u'Vanity Page Location'),
        description=_(u"Where in the site the user's vanity page is located."),
        required=False,
    )



class UserDataSchemaProvider(object):
    '''Utility that provides the vain user data schema on demand'''
    implements(IUserDataSchemaProvider)
    def getSchema(self):
        return IVainUserDataSchema


class VaneUserDataPanelAdapter(UserDataPanelAdapter):
    '''Add methods to get/set vanityPageUpdateDate.'''
    @property
    def vanityPageUpdateDate(self):
        '''Last time vanity page was updated'''
        value = self.context.getProperty('vanityPageUpdateDate', None)
        if value is None:
            return date.min
        elif isinstance(value, basestring):
            return date.strptime(value, '')
        elif isinstance(value, oldDateTime):
            dt = value.asdatetime()
            return date(dt.year, dt.month, dt.day)
        elif isinstance(value, datetime):
            return date(value.year, value.month, value.day)
        # Assume it's a date at this point
        return value
    @vanityPageUpdateDate.setter
    def vanityPageUpdateDate(self, value):
        return self.context.setMemberProperties({'vanityPageUpdateDate': value})
    @property
    def vanityPageLocation(self):
        '''Location of vanity page in the portal'''
        return self.context.getProperty('vanityPageLocation', None)
    @vanityPageLocation.setter
    def vanityPageLocation(self, value):
        return self.context.setMemberProperties({'vanityPageLocation': value})
    

