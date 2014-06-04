"""Definition of the MailTemplateTool content type
"""

from zope.interface import implements

from Products.CMFCore.utils import UniqueObject

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from zettwerk.mailtemplates.interfaces import IMailTemplateTool
from zettwerk.mailtemplates.config import PROJECTNAME

from Products.CMFCore.utils import getToolByName

from email.Utils import parseaddr
from email.Utils import formataddr


MailTemplateToolSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

MailTemplateToolSchema['title'].storage = atapi.AnnotationStorage()
MailTemplateToolSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    MailTemplateToolSchema,
    folderish=True,
    moveDiscussion=False
)


class MailTemplateTool(UniqueObject, folder.ATFolder):
    """Description of the Example Type"""

    implements(IMailTemplateTool)
    id = 'portal_mail_templates'

    meta_type = "MailTemplateTool"
    schema = MailTemplateToolSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

    def isOverwrittenDefaultTemplate(self, default_template_id):
        """ if the default template id matches 'registration' or
        'password_reset' - check the existance of these templates. """
        try:
            return self.getTemplate(default_template_id) is not None
        except ValueError:
            return False

    def getTemplate(self, template_id):
        """ return a template by template id """
        for template in self.values():
            if template.getTemplateId() == template_id:
                return template
        raise ValueError('Invalid template id')

    def sendTemplate(self, template_id, member_id, resetDict=None):
        """ send the chosen template_id to mto from mfrom
        fill the placeholder with values relating to member
        """
        template = self.getTemplate(template_id)
        mtool = getToolByName(self, 'portal_membership')
        ptool = getToolByName(self, 'portal_url')

        portal = ptool.getPortalObject()
        member = mtool.getMemberById(member_id)

        #get the recipient data from the member
        to_address = member.getProperty('email', '')
        if not to_address:
            to_address = member.getProperty('private_email', '')
        to_name = member.getProperty('fullname', '')
        mto = formataddr((to_name, to_address))
        if parseaddr(mto)[1] != to_address:
            mto = to_address

        #use the portal email and admin name as sender info
        from_address = portal.getProperty('email_from_address', '')
        from_name = portal.getProperty('email_from_name', '')
        mail_charset = portal.getProperty('email_charset', 'utf-8')

        mfrom = formataddr((from_name, from_address))
        if parseaddr(mfrom)[1] != from_address:
            mfrom = from_address

        if mto:
            body = template.getRenderedBody(member, **resetDict)
            subject = template.Title()

            mh = getToolByName(self, 'MailHost')
            mh.send(body,
                    mto=mto,
                    mfrom=mfrom,
                    subject=subject,
                    charset=mail_charset,
                    msg_type='text/plain')

atapi.registerType(MailTemplateTool, PROJECTNAME)
