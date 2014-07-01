# -*- extra stuff goes here -*-

from zope.i18nmessageid import MessageFactory
contentMessageFactory = MessageFactory('zettwerk.mobile')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
