# -*- coding: utf-8 -*-
"""Init and utils."""
from logging import getLogger
from zope.i18nmessageid import MessageFactory

rg_infocard_msgfactory = MessageFactory('rg.infocard')
rg_infocard_logger = getLogger('rg.infocard')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
