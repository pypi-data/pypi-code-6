from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class IUnprotectedRendered(Interface):
    """
    """


class UnprotectedRendered(BrowserView):
    """ used by mail_password_template (password reset) cause of
    security restrictions:

    In general, the portal_mail_templates tool is not accessable for anonymous
    users. This view bypasses the access to a template and renderes it for a
    given member. This is needed, for example, for sending password reset mails
    to anonymous users.
    """

    implements(IUnprotectedRendered)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, template_id, member):
        """ """
        template_tool = getToolByName(self.context, 'portal_mail_templates')

        data = {'has_template': template_tool.hasTemplate(template_id),
                'subject': '',
                'body': ''}

        if data['has_template']:
            template = template_tool.getTemplate(template_id)
            data['subject'] = template.Title()
            data['body'] = template.getRenderedBody(member)

        return data
