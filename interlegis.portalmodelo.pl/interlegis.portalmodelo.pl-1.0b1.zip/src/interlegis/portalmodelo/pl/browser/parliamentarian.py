# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield import DataGridFieldFactory
from five import grok
from interlegis.portalmodelo.pl.interfaces import IParliamentarian
from interlegis.portalmodelo.pl.interfaces import ISAPLMenuItem
from interlegis.portalmodelo.pl.utils import _get_legislatures
from plone.directives import dexterity
from plone.directives import form
from Products.CMFCore.interfaces import IFolderish
from z3c.form import field

grok.templatedir('templates')


class Parliamentarian_View(dexterity.DisplayForm):
    grok.context(IParliamentarian)
    grok.require('zope2.View')
    grok.name('view')


class AddForm(form.AddForm):
    # XXX: this is not working
    grok.name('add-Parliamentarian')
    grok.context(IFolderish)

    fields = field.Fields(IParliamentarian)
    fields['party_affiliation'].widgetFactory = DataGridFieldFactory

    def updateWidgets(self):
        super(AddForm, self).updateWidgets()
        self.widgets['party_affiliation'].allow_reorder = True
        self.widgets['party_affiliation'].auto_append = False


class EditForm(form.EditForm):
    grok.name('edit')
    grok.context(IParliamentarian)

    fields = field.Fields(IParliamentarian)
    fields['party_affiliation'].widgetFactory = DataGridFieldFactory

    def updateWidgets(self):
        super(EditForm, self).updateWidgets()
        self.widgets['party_affiliation'].allow_reorder = True
        self.widgets['party_affiliation'].auto_append = False


class Parliamentarians(grok.View):
    grok.context(ISAPLMenuItem)
    grok.require('zope2.View')

    def get_legislatures(self):
        return _get_legislatures()
