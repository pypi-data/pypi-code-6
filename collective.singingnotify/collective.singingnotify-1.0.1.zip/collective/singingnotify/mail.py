from Acquisition import aq_inner
from OFS.SimpleItem import SimpleItem
from zope.component import adapts
from zope.component.interfaces import ComponentLookupError
from zope.interface import Interface, implements
from zope.formlib import form

from plone.app.contentrules.browser.formhelper import AddForm, EditForm
from plone.contentrules.rule.interfaces import IRuleElementData, IExecutable

from Products.CMFCore.utils import getToolByName
from collective.singingnotify import MessageFactory as _
from collective.singingnotify import logger
from collective.singingnotify.interfaces import IUnsubscribeNotifyAction, IConfirmNotifyAction


class UnsubscribeNotifyAction(SimpleItem):
    """
    The implementation of the action defined before
    """
    implements(IUnsubscribeNotifyAction, IRuleElementData)

    subject = u''
    source = u''
    dest_addr = u''
    message = u''

    element = 'plone.actions.SingingUnsubscribeNotify'

    @property
    def summary(self):
        return _(u"Email report to ${dest_addr}",
                 mapping=dict(dest_addr=self.dest_addr))


class ConfirmNotifyAction(SimpleItem):
    """
    The implementation of the action defined before
    """
    implements(IConfirmNotifyAction, IRuleElementData)

    subject = u''
    source = u''
    dest_addr = u''
    message = u''

    element = 'plone.actions.NewsletterConfirmNotify'

    @property
    def summary(self):
        return _(u"Email report to ${dest_addr}",
                 mapping=dict(dest_addr=self.dest_addr))


class MailActionExecutor(object):
    """
    The executor for this action.
    """
    implements(IExecutable)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def send_mail(self, message, dest_addr, source_addr, subject):
        mailhost = getToolByName(aq_inner(self.context), "MailHost")
        if not mailhost:
            raise ComponentLookupError, 'You must have a Mailhost utility to \
execute this action'
        urltool = getToolByName(aq_inner(self.context), "portal_url")
        portal = urltool.getPortalObject()
        email_charset = portal.getProperty('email_charset')
        logger.info('sending to: %s' % dest_addr)
        try:
            # sending mail in Plone 4
            mailhost.send(message, mto=dest_addr, mfrom=source_addr,
                    subject=subject, charset=email_charset)
        except:
            #sending mail in Plone 3
            mailhost.secureSend(message, dest_addr, source_addr,
                    subject=subject, subtype='plain',
                    charset=email_charset, debug=False)

        return True


class MailActionUnsubscribeExecutor(MailActionExecutor):
    """
    The executor for this action.
    """
    adapts(Interface, IUnsubscribeNotifyAction, Interface)

    def __call__(self):
        source_addr = self.element.source
        dest_addr = self.element.dest_addr
        urltool = getToolByName(aq_inner(self.context), "portal_url")
        portal = urltool.getPortalObject()
        if not source_addr:
            # no source provided, looking for the site wide from email
            # address
            from_address = portal.getProperty('email_from_address')
            if not from_address:
                raise ValueError('You must provide a source address for this \
                                 action or enter an email in the portal properties')
            from_name = portal.getProperty('email_from_name')
            source_addr = "%s <%s>" % (from_name, from_address)

        obj = self.event.object
        folder_url = self.context.absolute_url()
        channel = getattr(obj, 'channel', None)
        composer_data = getattr(obj, 'composer_data', None)
        message = self.element.message
        message = message.replace("${url}", folder_url)
        message = message.replace("${portal}", portal.Title())
        if channel:
            message = message.replace("${channel}", channel.title)
        if composer_data:
            message = message.replace("${subscriber}", composer_data.get('email', ''))
        subject = self.element.subject
        subject = subject.replace("${url}", folder_url)
        subject = subject.replace("${portal}", portal.Title())
        return self.send_mail(message=message,
                              dest_addr=dest_addr,
                              source_addr=source_addr,
                              subject=subject)


class MailActionConfirmExecutor(MailActionExecutor):
    """
    The executor for this action.
    """
    adapts(Interface, IConfirmNotifyAction, Interface)

    def __call__(self):
        source_addr = self.element.source
        dest_addr = self.element.dest_addr
        urltool = getToolByName(aq_inner(self.context), "portal_url")
        portal = urltool.getPortalObject()
        if not source_addr:
            # no source provided, looking for the site wide from email
            # address
            from_address = portal.getProperty('email_from_address')
            if not from_address:
                raise ValueError('You must provide a source address for this \
                                 action or enter an email in the portal properties')
            from_name = portal.getProperty('email_from_name')
            source_addr = "%s <%s>" % (from_name, from_address)
        channel = self.event.object
        subscriber = self.event.subscriber
        composer_data = getattr(subscriber, 'composer_data', None)
        folder_url = self.context.absolute_url()
        message = self.element.message
        message = message.replace("${url}", folder_url)
        message = message.replace("${portal}", portal.Title())
        message = message.replace("${channel}", channel.title)
        if composer_data:
            message = message.replace("${subscriber}", composer_data.get('email', ''))
        subject = self.element.subject
        subject = subject.replace("${url}", folder_url)
        subject = subject.replace("${portal}", portal.Title())
        return self.send_mail(message=message,
                              dest_addr=dest_addr,
                              source_addr=source_addr,
                              subject=subject)


class UnsubscribeNotifyAddForm(AddForm):
    """
    An add form for the mail action
    """
    form_fields = form.FormFields(IUnsubscribeNotifyAction)
    label = _(u"Add S&D Unsubscription Mail Action")
    description = _(u"A mail action that sends email notify when an user will unsubscribe from a channel.")
    form_name = _(u"Configure element")

    def create(self, data):
        a = UnsubscribeNotifyAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class UnsubscribeNotifyEditForm(EditForm):
    """
    An edit form for the mail action
    """
    form_fields = form.FormFields(IUnsubscribeNotifyAction)
    label = _(u"Edit S&D Unsubscription Mail Action")
    description = _(u"A mail action that sends email notify when an user will unsubscribe from a channel.")
    form_name = _(u"Configure element")


class ConfirmNotifyAddForm(AddForm):
    """
    An add form for the mail action
    """
    form_fields = form.FormFields(IConfirmNotifyAction)
    label = _(u"Add S&D Confirm Subscription Mail Action")
    description = _(u"A mail action that sends email notify when an user confirm his subscription in a channel.")
    form_name = _(u"Configure element")

    def create(self, data):
        a = ConfirmNotifyAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class ConfirmNotifyEditForm(EditForm):
    """
    An edit form for the mail action
    """
    form_fields = form.FormFields(IConfirmNotifyAction)
    label = _(u"Edit S&D Confirm Subscription Mail Action")
    description = _(u"A mail action that sends email notify when an user confirm his subscription in a channel.")
    form_name = _(u"Configure element")
