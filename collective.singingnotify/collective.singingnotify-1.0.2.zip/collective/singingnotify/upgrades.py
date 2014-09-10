# -*- coding: utf-8 -*-
from collective.singingnotify import logger
from zope.component import getUtility
from plone.contentrules.engine.interfaces import IRuleStorage
from collective.dancing.events import IConfirmUnsubscriptionEvent
from collective.singingnotify.interfaces import IUnsubscribeNotifyAction
from zope.intid.interfaces import IIntIdRemovedEvent

default_profile = 'profile-collective.singingnotify:default'


def to_1100(context):
    """
    """
    logger.info('Upgrading collective.singingnotify to version 1.1.0')
    storage = getUtility(IRuleStorage)
    for rule in storage.values():
        for action in rule.actions:
            if IUnsubscribeNotifyAction.providedBy(action) and\
               rule.event == IIntIdRemovedEvent:
                rule.event = IConfirmUnsubscriptionEvent
    logger.info('Updated registered rules')
