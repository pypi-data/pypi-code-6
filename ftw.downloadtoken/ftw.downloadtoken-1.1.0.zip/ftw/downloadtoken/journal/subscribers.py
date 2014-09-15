from DateTime import DateTime
from ftw.downloadtoken import _
from ftw.journal.events.events import JournalEntryEvent
from zope.event import notify


def downloadlink_sent(event):
    emails = event.emails
    obj = event.obj
    action = _(
        u"label_send_dllink", default=u"Downloadlink sent",
        mapping=dict(
            mail_list=len(emails) > 0 and ', '.join(emails) + '\n' or '-'))
    time = DateTime()
    notify(JournalEntryEvent(obj, event.comment, action, time=time))


def downloadlink_opened(event):
    email = event.email
    obj = event.obj
    action = _(u"label_open_dllink", default=u"Downloadlink opened")
    time = DateTime()
    notify(JournalEntryEvent(obj, '-', action, actor=email, time=time))
