from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from shop.vitrine import MessageFactory as _
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
from zope.component import getMultiAdapter
# Interface class; used to define content-type schema.

# @grok.provider(IContextSourceBinder)
# def getTodasCategorias(context):
#     catalog = getToolByName(context, 'portal_catalog')
#     results = catalog(Type='Categoria') 
#     if results is not None:
#         ret = []
#         for result in results:
#             obj = result.getObject()
#             ret.append(SimpleVocabulary.createTerm(obj.id, str(obj.id), obj.title))
#         return SimpleVocabulary(ret)

@grok.provider(IContextSourceBinder)
def getCategoriasDoContexto(context):
    #catalog = getToolByName(context, 'portal_catalog')
    context = aq_inner(context)
    categorias = getattr(context, 'categorias')
    if categorias:
        ret = []
        for cat in categorias.keys():
            categoria = getattr(categorias, cat)
            if categoria.portal_type == 'shop.vitrine.categoria':
                ret.append(SimpleVocabulary.createTerm(categoria.id, str(categoria.id), categoria.title))
        return SimpleVocabulary(ret)

@grok.provider(IContextSourceBinder)
def getImages(context):
    imgs = context.keys()
    if imgs is not None:
        ret = []
        for img in imgs:
            obj = getattr(context, img)
            if obj.portal_type == 'Image':
                ret.append(SimpleVocabulary.createTerm(obj.id, str(obj.id), obj.title))
        return SimpleVocabulary(ret)

class IProduto(form.Schema, IImageScaleTraversable):
    """
    Item de venda
    """

    detalhes = RichText(title=_(u"Detalhes"), description=_(u"Detalhes do produto"))
    categoria = schema.Choice(title=_(u"Categoria"), 
                              description=_(u"Categoria do produto"),
                              required = False, 
                              source = getCategoriasDoContexto)

    imagem = schema.Choice(title=_(u"Imagem"), 
                              description=_(u"Imagem principal"),
                              required = False, 
                              source = getImages)

class Produto(Container):
    grok.implements(IProduto)

    # Add your class methods and properties here

    pass

# scratch = cocar
# itch

class View(grok.View):
    """ sample view class """

    grok.context(IProduto)
    grok.require('zope2.View')

    # grok.name('view')
    # Add view methods here
    
    def getImagens(self):
        context = aq_inner(self.context)
        imgs = context.keys()
        if imgs is not None:
            ret = []
            for img in imgs:
                obj = getattr(context, img)
                if obj.portal_type == 'Image':
                    ret.append(obj)
            return ret

    def getTamanhos(self):
        context = aq_inner(self.context)
        imgs = context.keys()
        if imgs is not None:
            ret = []
            for img in imgs:
                obj = getattr(context, img)
                if obj.portal_type == 'shop.vitrine.size':
                    ret.append(obj)
            return ret
        
    def getAuthenticatedUser(self):
        ps = getMultiAdapter((self.context, self.request), name="plone_portal_state")
        return ps.member()
        
    def getGroupsFromUser(self, user = None):
        mt = getToolByName(self.context, 'portal_groups')
        if user is None:
            user = self.getAuthenticatedUser()
        groups = mt.getGroupsByUserId(user)
        grp = []
        for group in groups:
            grp.append(str(group))
        return grp
    