#-*- coding: utf-8 -*-
from zope.component.hooks import getSite
from z3c.form import interfaces

from zope import schema
from zope.interface import Interface

from zope.i18nmessageid import MessageFactory

#site_url = getSite().absolute_url()

_ = MessageFactory('ityou.notify')

class INotifySettings(Interface):
    """Global Notify settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    astream_notifications_active = schema.Bool(title=_(u"Send Activity Stream mails"),
                                  description=_(u'help_astream_notification_status',
                                                default=u"Should ityou.notify send mails when documents are addes/mofified?"),
                                  required=False,
                                  default=False,)

    imessage_notifications_active = schema.Bool(title=_(u"Send iMessage mails"),
                                  description=_(u'help_imessage_notification_status',
                                                default=u"Should ityou.notify send mails when new messages are created?"),
                                  required=False,
                                  default=False,)

    site_url = schema.TextLine(title=_(u"Site URL"),
                                  description=_(u'help_site_url',
                                                default=u"Define the site URL for the outgoing eMails. The URL is needed to compose the links in the emails. Don't use a trailing slash. "),
                                  required=True,
                                  )

    email_header = schema.Text(title=_(u"Mail header"),
                                  description=_(u'help_email_header',
                                                default=u"Define the header for the outgoing eMails"),
                                  required=False)

    email_footer = schema.Text(title=_(u"Mail footer"),
                                  description=_(u'help_mail_footer',
                                                default=u"Define the footer for the outgoing eMails"),
                                  required=False)

class INotify(Interface):
    """Marker Interface
    """
