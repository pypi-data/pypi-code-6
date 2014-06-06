"""Definition of the Template content type
"""

from zope.interface import implements

from DateTime import DateTime
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-
from zettwerk.mailtemplates import mailtemplatesMessageFactory as _

from zettwerk.mailtemplates.interfaces import ITemplate
from zettwerk.mailtemplates.config import PROJECTNAME

from Products.CMFCore.utils import getToolByName


TemplateSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'templateId',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Template id"),
            description=_(u"a unique id for the template. You can use a " \
                              " custom one or use one of the defaults: " \
                              "'registration', 'password_reset'"),
        ),
        required=True,
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

TemplateSchema['title'].storage = atapi.AnnotationStorage()
TemplateSchema['title'].widget.label = 'Subject'
TemplateSchema['title'].widget.description = 'Enter the mail subject'

TemplateSchema['description'].storage = atapi.AnnotationStorage()
TemplateSchema['description'].widget.label = 'Mail body text'
TemplateSchema['description'].widget.description = '''
You can use python string substitution syntax to insert dynamic values.
Supported keywords are: username, fullname, portal_url, portal_name,
password_reset_link, expires_string. Example: "Hello %(fullname)s"
'''

schemata.finalizeATCTSchema(TemplateSchema, moveDiscussion=False)


class Template(base.ATCTContent):
    """Description of the Example Type"""
    implements(ITemplate)

    meta_type = "Template"
    schema = TemplateSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    templateId = atapi.ATFieldProperty('templateId')

    def getSubject(self):
        """ return the title """
        return self.Title()

    def getBody(self):
        """ return the description """
        return self.Description()

    def getRenderedBody(self, member, preview=False):
        """ will fail on invalid substitutions
        returns empty strings if the member does not
        have the information or is empty
        """
        ptool = getToolByName(self, 'portal_url')
        rtool = getToolByName(self, 'portal_password_reset')

        portal_url = ptool()
        portal_name = ptool.getProperty('title', '')
        username = member.getId()
        fullname = member.getProperty('fullname', '')

        data = {'username': username,
                'fullname': fullname,
                'portal_url': portal_url,
                'portal_name': portal_name}

        body = self.getBody()
        if not preview:
            if body.find('%(password_reset_link)') != -1 or \
                    body.find('%(expires_string)') != -1:
                ## returns a dict with reset data
                reset = rtool.requestReset(username)
                data.update(
                    {'passwort_reset_link':
                         rtool.pwreset_constructURL(reset['randomstring'])}
                    )
                data.update(
                    {'expires_string':
                         self.toLocalizedTime(reset['expires'], long_format=1)}
                    )

        else:
            data.update(
                {'passwort_reset_link': data['portal_url']}
                )
            data.update(
                {'expires_string':
                     self.toLocalizedTime(DateTime(), long_format=1)}
                )

        return body % data

    def getRenderedBodyPreview(self):
        """ return the rendered mail text, will not fail on errors,
        and decoded for gui """
        mtool = getToolByName(self, 'portal_membership')
        ptool = getToolByName(self, 'portal_properties')
        output_enc = ptool.site_properties.getProperty('default_charset')

        try:
            body = self.getRenderedBody(mtool.getAuthenticatedMember(),
                                        preview=True)
            if output_enc != 'utf-8':
                return body.encode(output_enc)
            else:
                return body
        except:
            return 'ERROR'

atapi.registerType(Template, PROJECTNAME)
