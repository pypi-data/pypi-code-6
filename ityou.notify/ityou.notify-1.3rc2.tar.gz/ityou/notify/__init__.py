# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("ityou.notify")

# Apps that can send notifications
ASTREAM      = "astream"
IMESSAGE     = "imessage"

# DEBUG = True -> send email to debug-email address
DEBUG = False   
DEBUG_EMAIL_ADR = 'XXXXX@YYYYYY.ZZ'

# /DEBUG -----------------------------------------

# --- mail template
# TODO: Übersetzungen
SUBJECT = {
    "astream"    : _(u"Document(s) had been created/updated"),
    "imessage"   : _(u"New message from %(sender_name)s")
}

BODY = {
    "astream"   : _(u"Hello %(receiver_name)s, \n\nhere is a list of newly created or modified documents:\n\n %(body)s \n\n"),
    "imessage"  : _(u"Hello %(receiver_name)s, \n\nYou received a new message from %(sender_name)s:\n\n\t<------ Begin ----------------->\n\n\t%(message)s\n\n\t<------ End ------------------->\nPlease click here to see the message:\n\n%(content_url)s\n\n")
}


# --- /mail template

# --- /Notify Mail params ------------------------


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
