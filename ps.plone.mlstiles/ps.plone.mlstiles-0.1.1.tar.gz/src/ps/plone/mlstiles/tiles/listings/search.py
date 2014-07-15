# -*- coding: utf-8 -*-
"""MLS listing search tile."""

# zope imports
from Acquisition import aq_inner
from Products.CMFPlone import PloneMessageFactory as PMF
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cover import _ as _cc
from collective.cover.tiles import base
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone.app.uuid.utils import uuidToObject
from plone.directives import form
from plone.mls.listing.browser import listing_search
from plone.mls.listing.browser.valuerange.widget import ValueRangeFieldWidget
from plone.mls.listing.i18n import _ as _mls
from plone.tiles.interfaces import (
    ITileDataManager,
    ITileType,
)
from plone.uuid.interfaces import IUUID
from z3c.form import button, field
from z3c.form.browser import checkbox, radio
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import queryUtility
from zope.interface import alsoProvides, implementer
from zope.schema import getFieldNamesInOrder
from zope.schema.fieldproperty import FieldProperty

# starting from 0.6.0 version plone.z3cform has IWrappedForm interface
try:
    from plone.z3cform.interfaces import IWrappedForm
    HAS_WRAPPED_FORM = True
except ImportError:
    HAS_WRAPPED_FORM = False

# local imports
from ps.plone.mlstiles import _


class ListingSearchForm(form.Form):
    """Listing Search Form."""
    fields = field.Fields(listing_search.IListingSearchForm)
    ignoreContext = True
    method = 'get'
    search_url = None

    fields['air_condition'].widgetFactory = radio.RadioFieldWidget
    fields['baths'].widgetFactory = ValueRangeFieldWidget
    fields['lot_size'].widgetFactory = ValueRangeFieldWidget
    fields['interior_area'].widgetFactory = ValueRangeFieldWidget
    fields['beds'].widgetFactory = ValueRangeFieldWidget
    fields['geographic_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['jacuzzi'].widgetFactory = radio.RadioFieldWidget
    fields['listing_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['location_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['object_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['ownership_type'].widgetFactory = checkbox.CheckBoxFieldWidget
    fields['pool'].widgetFactory = radio.RadioFieldWidget
    fields['view_type'].widgetFactory = checkbox.CheckBoxFieldWidget

    @property
    def action(self):
        """See interfaces.IInputForm"""
        if self.search_url:
            return self.search_url
        return super(ListingSearchForm, self).action()

    @button.buttonAndHandler(
        PMF(u'label_search', default=u'Search'),
        name='search',
    )
    def handle_search(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return


class IListingSearchTile(base.IPersistentCoverTile):
    """Configuration schema for a listing search."""

    header = schema.TextLine(
        required=False,
        title=_cc(u'Header'),
    )

    form.omitted('form_listing_type')
    form.no_omit(IDefaultConfigureForm, 'form_listing_type')
    form_listing_type = schema.Text(
        required=False,
        title=_mls(u'Listing Type'),
    )

    form.omitted('form_location_state')
    form.no_omit(IDefaultConfigureForm, 'form_location_state')
    form_location_state = schema.Text(
        required=False,
        title=_mls(u'State'),
    )

    form.omitted('form_location_county')
    form.no_omit(IDefaultConfigureForm, 'form_location_county')
    form_location_county = schema.Text(
        required=False,
        title=_mls(u'County'),
    )

    form.omitted('form_location_district')
    form.no_omit(IDefaultConfigureForm, 'form_location_district')
    form_location_district = schema.Text(
        required=False,
        title=_mls(u'District'),
    )

    form.omitted('form_location_city')
    form.no_omit(IDefaultConfigureForm, 'form_location_city')
    form_location_city = schema.Text(
        required=False,
        title=_mls(u'City/Town'),
    )

    form.omitted('form_price_min')
    form.no_omit(IDefaultConfigureForm, 'form_price_min')
    form_price_min = schema.Text(
        required=False,
        title=_mls(u'Price (Min)'),
    )

    form.omitted('form_price_max')
    form.no_omit(IDefaultConfigureForm, 'form_price_max')
    form_price_max = schema.Text(
        required=False,
        title=_mls(u'Price (Max)'),
    )

    form.omitted('form_location_type')
    form.no_omit(IDefaultConfigureForm, 'form_location_type')
    form_location_type = schema.Text(
        required=False,
        title=_mls(u'Location Type'),
    )

    form.omitted('form_geographic_type')
    form.no_omit(IDefaultConfigureForm, 'form_geographic_type')
    form_geographic_type = schema.Text(
        required=False,
        title=_mls(u'Geographic Type'),
    )

    form.omitted('form_view_type')
    form.no_omit(IDefaultConfigureForm, 'form_view_type')
    form_view_type = schema.Text(
        required=False,
        title=_mls(u'View Type'),
    )

    form.omitted('form_object_type')
    form.no_omit(IDefaultConfigureForm, 'form_object_type')
    form_object_type = schema.Text(
        required=False,
        title=_mls(u'Object Type'),
    )

    form.omitted('form_ownership_type')
    form.no_omit(IDefaultConfigureForm, 'form_ownership_type')
    form_ownership_type = schema.Text(
        required=False,
        title=_mls(u'Ownership Type'),
    )

    form.omitted('form_beds')
    form.no_omit(IDefaultConfigureForm, 'form_beds')
    form_beds = schema.Text(
        required=False,
        title=_mls(u'Bedrooms'),
    )

    form.omitted('form_baths')
    form.no_omit(IDefaultConfigureForm, 'form_baths')
    form_baths = schema.Text(
        required=False,
        title=_mls(u'Bathrooms'),
    )

    form.omitted('form_air_condition')
    form.no_omit(IDefaultConfigureForm, 'form_air_condition')
    form_air_condition = schema.Text(
        required=False,
        title=_mls(u'Air Condition'),
    )

    form.omitted('form_pool')
    form.no_omit(IDefaultConfigureForm, 'form_pool')
    form_pool = schema.Text(
        required=False,
        title=_mls(u'Pool'),
    )

    form.omitted('form_jacuzzi')
    form.no_omit(IDefaultConfigureForm, 'form_jacuzzi')
    form_jacuzzi = schema.Text(
        required=False,
        title=_mls(u'Jacuzzi'),
    )

    form.omitted('form_lot_size')
    form.no_omit(IDefaultConfigureForm, 'form_lot_size')
    form_lot_size = schema.Text(
        required=False,
        title=_mls(u'Lot Size'),
    )

    form.omitted('form_interior_area')
    form.no_omit(IDefaultConfigureForm, 'form_interior_area')
    form_interior_area = schema.Text(
        required=False,
        title=_mls(u'Interior Area'),
    )

    footer = schema.TextLine(
        required=False,
        title=_cc(u'Footer'),
    )

    uuid = schema.TextLine(
        readonly=True,
        title=_cc(u'UUID'),
    )


@implementer(IListingSearchTile)
class ListingSearchTile(base.PersistentCoverTile):
    """A tile that shows a search form for listings."""

    is_configurable = True
    is_editable = True
    short_name = _(u'MLS: Listing Search')
    index = ViewPageTemplateFile('search.pt')

    header = FieldProperty(IListingSearchTile['header'])

    form_listing_type = FieldProperty(IListingSearchTile['form_listing_type'])
    form_location_state = FieldProperty(
        IListingSearchTile['form_location_state']
    )
    form_location_county = FieldProperty(
        IListingSearchTile['form_location_county']
    )
    form_location_district = FieldProperty(
        IListingSearchTile['form_location_district']
    )
    form_location_city = FieldProperty(
        IListingSearchTile['form_location_city']
    )
    form_price_min = FieldProperty(IListingSearchTile['form_price_min'])
    form_price_max = FieldProperty(IListingSearchTile['form_price_max'])
    form_location_type = FieldProperty(
        IListingSearchTile['form_location_type']
    )
    form_geographic_type = FieldProperty(
        IListingSearchTile['form_geographic_type']
    )
    form_view_type = FieldProperty(IListingSearchTile['form_view_type'])
    form_object_type = FieldProperty(IListingSearchTile['form_object_type'])
    form_ownership_type = FieldProperty(
        IListingSearchTile['form_ownership_type']
    )
    form_beds = FieldProperty(IListingSearchTile['form_beds'])
    form_baths = FieldProperty(IListingSearchTile['form_baths'])
    form_air_condition = FieldProperty(
        IListingSearchTile['form_air_condition']
    )
    form_pool = FieldProperty(IListingSearchTile['form_pool'])
    form_jacuzzi = FieldProperty(IListingSearchTile['form_jacuzzi'])
    form_lot_size = FieldProperty(IListingSearchTile['form_lot_size'])
    form_interior_area = FieldProperty(
        IListingSearchTile['form_interior_area']
    )

    footer = FieldProperty(IListingSearchTile['footer'])
    uuid = FieldProperty(IListingSearchTile['uuid'])

    def get_title(self):
        return self.data['title']

    def has_listing_search(self, obj):
        """Check if the obj is activated for a listing search."""
        return listing_search.IListingSearch.providedBy(obj)

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(listing_search.CONFIGURATION_KEY, {})

    def is_empty(self):
        return self.data.get('uuid', None) is None or \
            uuidToObject(self.data.get('uuid')) is None

    def populate_with_object(self, obj):
        # Check permission.
        super(ListingSearchTile, self).populate_with_object(obj)

        if obj.portal_type in self.accepted_ct():
            # Use obj's title as header.
            header = safe_unicode(obj.Title())
            footer = _cc(u'More…')
            uuid = IUUID(obj)

            data_mgr = ITileDataManager(self)
            data_mgr.set({
                'header': header,
                'footer': footer,
                'uuid': uuid,
            })

    def remove_relation(self):
        data_mgr = ITileDataManager(self)
        old_data = data_mgr.get()
        if 'uuid' in old_data:
            old_data.pop('uuid')
        data_mgr.set(old_data)

    def show_header(self):
        return self._field_is_visible('header')

    @property
    def search_form(self):
        uuid = self.data.get('uuid', None)
        obj = uuidToObject(uuid)
        if not self.has_listing_search(obj):
            return

        available_fields = []
        tileType = queryUtility(ITileType, name=self.__name__)
        conf = self.get_tile_configuration()
        for name in getFieldNamesInOrder(tileType.schema):
            if name in conf:
                field_conf = conf[name]
                if ('visibility' in field_conf and
                        field_conf['visibility'] == u'off'):
                    # If the field was configured to be invisible, then just
                    # ignore it
                    continue
            if name.startswith('form_'):
                available_fields.append(name.split('form_')[1])

        search_form = ListingSearchForm(aq_inner(obj), self.request)
        search_form.fields = search_form.fields.select(*available_fields)
        search_form.search_url = self.search_url()
        if HAS_WRAPPED_FORM:
            alsoProvides(search_form, IWrappedForm)
        search_form.update()
        return search_form

    def search_url(self):
        uuid = self.data.get('uuid', None)
        obj = uuidToObject(uuid)
        return obj.absolute_url() if obj else ''

    def show_footer(self):
        return self._field_is_visible('footer')
