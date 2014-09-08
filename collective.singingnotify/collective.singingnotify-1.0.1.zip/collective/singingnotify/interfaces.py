# -*- coding: utf-8 -*-
from collective.singingnotify import MessageFactory as _
from zope.interface import Interface
from zope import schema


class IUnsubscribeNotifyAction(Interface):
    """Definition of the configuration available for a mail action
    """
    subject = schema.TextLine(
        title=_(u"Subject"),
        description=_(u"Subject of the message"),
        required=True
        )

    source = schema.TextLine(
        title=_(u"Sender email"),
        description=_("The email address that sends the email. If no email is \
            provided here, it will use the portal from address."),
         required=False
         )

    dest_addr = schema.TextLine(
        title=_(u"Receiver email"),
        description=_("The address where you want to send the e-mail message."),
        required=True
        )

    message = schema.Text(
        title=_(u"Message"),
        description=_(u"Type in here the message that you want to mail. Some \
            defined content can be replaced: ${portal} will be replaced by the title \
            of the portal. ${url} will be replaced by the URL of the newsletter. \
            ${channel} will be replaced by the newsletter channel name. ${subscriber} will be replaced by subscriber name."),
        required=True
        )


class IConfirmNotifyAction(Interface):
    """Definition of the configuration available for a mail action
    """
    subject = schema.TextLine(
        title=_(u"Subject"),
        description=_(u"Subject of the message"),
        required=True
        )

    source = schema.TextLine(
        title=_(u"Sender email"),
        description=_("The email address that sends the email. If no email is \
            provided here, it will use the portal from address."),
         required=False
         )

    dest_addr = schema.TextLine(
        title=_(u"Receiver email"),
        description=_("The address where you want to send the e-mail message."),
        required=True
        )

    message = schema.Text(
        title=_(u"Message"),
        description=_(u"Type in here the message that you want to mail. Some \
            defined content can be replaced: ${portal} will be replaced by the title \
            of the portal. ${url} will be replaced by the URL of the newsletter. \
            ${channel} will be replaced by the newsletter channel name. ${subscriber} will be replaced by subscriber name."),
        required=True
        )
