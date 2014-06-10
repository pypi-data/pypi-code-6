# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.app.portlets.browser import formhelper
from plone.portlets.interfaces import IPortletDataProvider
from rt.maracas import _
from zope import schema
from zope.formlib import form
from zope.interface import implements


class IRtMaracasPortlet(IPortletDataProvider):
    """A portlet which renders the results of a collection object.
    """
    title = schema.TextLine(
        title=_(u"Title"),
        description=_(u"Title of the maracas portlet"),
        required=True
    )
    maraca_type = schema.Choice(
        title=_(u"Type of maracas"),
        description=_(
            (
                u"You can choose between a vanilla maracas "
                u"or maracas with wistle"
            )
        ),
        values=(
            u'maracas_simple',
            u'maracas_whistle'
        ),
        default=u'maracas_simple',
        required=True,
    )
    autoplay = schema.Bool(
        title=_(u"Autoplay"),
        description=_(
            u"Tick this if you want to display the media with autoplay"
        ),
        required=True,
        default=False,
    )
    controls = schema.Bool(
        title=_(u"Controls"),
        description=_(
            u"Tick this if you want to display the media with controls"
        ),
        required=True,
        default=False
    )
    loop = schema.Bool(
        title=_(u"Loop"),
        description=_(
            u"Tick this if you want the media to loop"
        ),
        required=True,
        default=False
    )


class Assignment(base.Assignment):
    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    implements(IRtMaracasPortlet)
    title = u""
    maraca_type = u"maracas_simple"
    autoplay = False
    controls = False
    loop = False

    def __init__(
        self,
        title=u"",
        maraca_type=u"maracas_simple",
        autoplay=False,
        controls=False,
        loop=False
    ):
        self.title = title
        self.maraca_type = maraca_type
        self.autoplay = autoplay
        self.controls = controls
        self.loop = loop


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('base.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def maracas(self):
        ''' Return a dict with some options
        '''
        maracas = {}
        for key in ('controls', 'autoplay', 'loop'):
            value = getattr(self.data, key, None)
            if value:
                maracas[key] = key
        return maracas


class AddForm(formhelper.AddForm):
    form_fields = form.Fields(IRtMaracasPortlet)
    label = _(u"Add Maracas Portlet")
    description = _(u"This portlet renders an audio tag to listen maracas")

    def create(self, data):
        return Assignment(**data)


class EditForm(formhelper.EditForm):
    form_fields = form.Fields(IRtMaracasPortlet)
    label = _(u"Edit Maracas Portlet")
    description = _(u"This portlet renders an audio tag to listen maracas")
