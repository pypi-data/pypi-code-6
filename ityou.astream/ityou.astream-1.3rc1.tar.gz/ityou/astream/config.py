# -*- coding: utf-8 -*-
from . import _
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

DEBUG       = False

NO_MESSAGES_ON_WORKFLOW_CHANGE = ['hide','retract']

ACTIVITY_STREAM = '@@activity-stream'
USER_ID_BLACKLIST = ['admin']
MESSAGE_TEXT_CONTAINER = {
    'title':        _(u'has edited the title of ${icon}${tag}${name}</i>.'),
    'description':  _(u'has edited the description of ${icon}${tag}${name}s</i>.'),
    'text':         _(u'has edited the content of ${icon}${tag}${name}</i>.'),
    'create':       _(u'has created ${icon}${tag}${name}</i>.'),
    'copy':         _(u'has copied ${icon}${tag}${name}</i>.'),
    'undefined':    _(u'has edited/created ${icon}${tag}${name}</i>.'),
    'edit':         _(u'has edited ${icon}${tag}${name}</i>.')
}                   
TIME_STRING = u"%d.%m.%Y - %H:%M"
MIN_ASTREAM_DELAY = 4000
ICON_TAG = "<img class='file-icon' src='%s' />"
