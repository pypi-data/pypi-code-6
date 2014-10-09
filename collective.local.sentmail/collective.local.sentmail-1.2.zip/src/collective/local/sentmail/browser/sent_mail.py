from plone import api
from email.utils import formataddr
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SentMailView(BrowserView):
    index = ViewPageTemplateFile('templates/sent_mail.pt')

    def get_user_info(self, userid):
        user = api.user.get(userid=userid)
        if user is None:
            recipient = userid
        else:
            recipient_fullname = user.getProperty('fullname', None) or \
                    user.getUserName()
            recipient_email = user.getProperty('email')
            if recipient_email:
                recipient = formataddr((recipient_fullname, recipient_email))
            else:
                recipient = recipient_fullname

        return recipient

    def __call__(self):
        self.mfrom = self.get_user_info(self.context.Creator())
        self.mto = []
        for userid in self.context.recipients:
            recipient = self.get_user_info(userid)
            self.mto.append(recipient)

        return self.index()
