from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Item

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone import api
from plone.api.exc import UserNotFoundError
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from Products.ATContentTypes.interface import IATFolder
from AccessControl import getSecurityManager

from tutorate.contenttypes import MessageFactory as _


# Interface class; used to define content-type schema.

class ISession(form.Schema, IImageScaleTraversable):
    """
    Session
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/session.xml to define the content type.

    #form.model("models/session.xml")
    topics = RichText(
            title=_(u"Topics"),
            description=_(u"areas to be covered"),
            required=False,
        ) 
    audience = RichText(
            title=_(u"Audience"),
            description=_(u"Your intended audience (e.g. startups, business persons, educators, web designers, programmers etc..)"),
            required=False,
        )
    google_form_key = schema.Text(
            title=_(u"Sign Up Form Key"),
            description=_(u"Form Key of Google Form, for older Google Forms add a ':' at the end of the Key"),
            required=False,
        )
    google_form_height = schema.Int(
            title=_(u"Sign Up Form Height"),
            description=_(u"Height of Google Form"),
            default=1300,
        )
    details = RichText(
            title=_(u"Details"),
            description=_(u"a more detailed overview"),
            required=False,
        )

    image = NamedBlobImage(
        title=_(u"Profile picture"),
        required=False,
    )



# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Session(Item):
    grok.implements(ISession)

    # Add your class methods and properties here
    pass


# View class
# The view will automatically use a similarly named template in
# session_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SessionListing(grok.View):
    grok.context(IATFolder)
    grok.require('zope2.View')

    

class View(grok.View):
    """ session view class """

    grok.context(ISession)
    grok.require('zope2.View')

    def google_form_url_valid(self):
        context = self.context.aq_inner
        formkey = context.google_form_key
        if formkey:
            if len(formkey) > 14:
                return True
        return False

    def google_form_url(self):
        context = self.context.aq_inner
        formkey = context.google_form_key

        if "-" in formkey:
            # new style form
            url = "https://docs.google.com/forms/d/%s/viewform?embedded=true"  % formkey
        else:
            # old style form
            url = "https://docs.google.com/spreadsheet/embeddedform?formkey=%s" % formkey        
        return url


    def can_edit(self):
        user = api.user.get_current()
        try:
            permissions = api.user.get_permissions(username=user.id, 
                              obj=self.context) 
            can_edit_ = permissions['Modify portal content']           
        except UserNotFoundError:
            # check if they are an admin
            user = getSecurityManager().getUser()
            can_edit_ = 'Manager' in user.getRoles() 
        return can_edit_

    # grok.name('view')

    # Add view methods here
