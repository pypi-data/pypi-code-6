from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Item

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable


from shop.vitrine import MessageFactory as _

# Interface class; used to define content-type schema.

class ISize(form.Schema, IImageScaleTraversable):
    """
    Size
    """
    #form.model("models/size.xml")
    Width  = schema.Float(title=_(u"Width"),  description=_(u"Product Width"))
    Height = schema.Float(title=_(u"Height"), description=_(u"Product Height"))
    Length = schema.Float(title=_(u"Lenth"),  description=_(u"Product Length"))
    Weight = schema.Float(title=_(u"Weight"), description=_(u"Product Weight"))
    Price =  schema.Float(title=_(u"Price"),  description=_(u"Product Price"))
    
    #form.omitted('Description')
    
# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Size(Item):
    grok.implements(ISize)

    # Add your class methods and properties here
    pass


# View class
# The view will automatically use a similarly named template in
# size_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(ISize)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
