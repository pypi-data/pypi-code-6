# -*- coding: utf-8 -*-

import logging
from AccessControl import ModuleSecurityInfo
from zope.i18nmessageid import MessageFactory


logger = logging.getLogger('collective.contactauthor')
messageFactory = MessageFactory('collective.contactauthor')
ModuleSecurityInfo('collective.contactauthor').declarePublic('messageFactory')

def initialize(context):
    pass