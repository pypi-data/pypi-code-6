# -*- coding: utf-8 -*-
from ..models.infocardcontainer import IInfocardcontainer
from Products.CMFPlone import PloneMessageFactory as __
from five import grok
from plone import api
from plone.directives.form import Schema, SchemaForm
from rg.infocard import rg_infocard_msgfactory as _
from rg.infocard.vocs.infocard_locations import InfocardLocations
from rg.infocard.vocs.infocard_recipients import InfocardRecipients
from z3c.form import button
from zope import schema
from zope.interface import invariant, Invalid


class IInfocardcontainerSearchForm(Schema):
    """ Define form fields """
    text = schema.TextLine(
        title=__(
            'label_search_text',
        ),
        required=False,
    )
    location = schema.Choice(
        title=_(
            'label_where_is_it',
            u"Where is it?"
        ),
        source=InfocardLocations,
        required=False,
    )
    recipient = schema.Choice(
        title=_(
            'label_for_who_is_it',
            u"For who is it?"
        ),
        source=InfocardRecipients,
        required=False,
    )

    @invariant
    def at_least_one(data):
        if data.location or data.recipient or data.text:
            return
        raise Invalid(
            _(
                'label_at_least_one_search_parameter',
                u'You should specify at least one search parameter'
            )
        )


class Form(SchemaForm):
    '''
    '''
    grok.name('view')
    grok.require('zope2.View')
    grok.context(IInfocardcontainer)

    @property
    def template(self):
        return grok.PageTemplateFile('templates/infocardcontainer_search.pt')

    ignoreContext = True

    schema = IInfocardcontainerSearchForm

    label = u""
    description = u""

    table_fields = [
        {
            'id': 'title',
            'label': __('title'),
        },
        {
            'id': 'description',
            'label': __('description'),
        },
        {
            'id': 'locations',
            'label': _(
                'label_where_is_it',
                u"Where is it?"
            ),
        },
        {
            'id': 'recipients',
            'label': _(
                'label_for_who_is_it',
                u"For who is it?"
            ),
        },
    ]

    def accept_infocard(self, infocard, data):
        ''' Given the data in the parameters filter the infocard
        '''
        if data.get('location'):
            if not data.get('location') in infocard.locations:
                return False
        if data.get('recipient'):
            if not data.get('recipient') in infocard.recipients:
                return False
        if data.get('text'):
            infocard_view = api.content.get_view('view', infocard, self.request)  # noqa
            if not data.get('text').lower() in infocard_view.searched_text:
                return False
        return True

    def search_results(self, data):
        '''
        '''
        infocards = self.context.listFolderContents(
            {'portal_type': 'infocard'}
        )
        results = []
        for infocard in infocards:
            if self.accept_infocard(infocard, data):
                infocard_view = api.content.get_view('view', infocard, self.request)  # noqa
                results.append(
                    {
                        'review_state': api.content.get_state(infocard),
                        'url': infocard.absolute_url,
                        'title': infocard.title,
                        'description': infocard.description,
                        'locations': infocard_view.locations,
                        'recipients': infocard_view.recipients,
                    },
                )
        sorted(results, key=lambda x: x['title'])
        return results

    @button.buttonAndHandler(__('label_search', u'Search'))
    def handleSearch(self, action):
        self.searching = True
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            self.results = []
            return
        self.results = self.search_results(data)

    @button.buttonAndHandler(__('label_cancel', u'Cancel'))
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
