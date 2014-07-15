# -*- coding: utf-8 -*-
"""MLS listing collection tiles."""

# python imports
import copy

# zope imports
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.cover import _ as _cc
from collective.cover.tiles import (
    base,
    configuration_view,
)
from plone.app.uuid.utils import uuidToObject
from plone.directives import form
from plone.memoize import view
from plone.mls.listing import api
from plone.mls.listing.browser import (
    listing_collection,
    recent_listings,
)
from plone.mls.listing.i18n import _ as _mls
from plone.namedfile.field import NamedBlobImage as NamedImage
from plone.tiles.interfaces import (
    ITileDataManager,
    ITileType,
)
from plone.uuid.interfaces import IUUID
from ps.plone.mls.browser.listings import featured
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import queryUtility
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty

# local imports
from ps.plone.mlstiles import _


class IListingCollectionTile(base.IPersistentCoverTile):
    """Configuration schema for a listing collection."""

    header = schema.TextLine(
        required=False,
        title=_cc(u'Header'),
    )

    form.omitted('count')
    form.no_omit(configuration_view.IDefaultConfigureForm, 'count')
    count = schema.List(
        required=False,
        title=_cc(u'Number of items to display'),
        value_type=schema.TextLine(),
    )

    form.omitted('offset')
    form.no_omit(configuration_view.IDefaultConfigureForm, 'offset')
    offset = schema.Int(
        default=0,
        required=False,
        title=_cc(u'Start at item'),
    )

    form.omitted('title')
    form.no_omit(configuration_view.IDefaultConfigureForm, 'title')
    title = schema.TextLine(
        required=False,
        title=_cc(u'Title'),
    )

    form.omitted('image')
    form.no_omit(configuration_view.IDefaultConfigureForm, 'image')
    image = NamedImage(
        required=False,
        title=_cc(u'Image'),
    )

    form.omitted('price')
    form.no_omit(configuration_view.IDefaultConfigureForm, 'price')
    form.widget(price='ps.plone.mlstiles.widgets.ListingTextFieldWidget')
    price = schema.TextLine(
        required=False,
        title=_mls(u'Price'),
    )

    form.omitted('workflow_status')
    form.no_omit(configuration_view.IDefaultConfigureForm, 'workflow_status')
    form.widget(
        workflow_status='ps.plone.mlstiles.widgets.ListingTextFieldWidget',
    )
    workflow_status = schema.TextLine(
        required=False,
        title=_mls(u'Workflow Status'),
    )

    form.omitted('listing_type')
    form.no_omit(configuration_view.IDefaultConfigureForm, 'listing_type')
    form.widget(
        listing_type='ps.plone.mlstiles.widgets.ListingTextFieldWidget',
    )
    listing_type = schema.TextLine(
        required=False,
        title=_mls(u'Listing Type'),
    )

    form.omitted('image_count')
    form.no_omit(configuration_view.IDefaultConfigureForm, 'image_count')
    form.widget(image_count='ps.plone.mlstiles.widgets.ListingTextFieldWidget')
    image_count = schema.TextLine(
        required=False,
        title=_mls(u'Image Count'),
    )

    form.omitted('object_type')
    form.no_omit(configuration_view.IDefaultConfigureForm, 'object_type')
    form.widget(object_type='ps.plone.mlstiles.widgets.ListingTextFieldWidget')
    object_type = schema.TextLine(
        required=False,
        title=_mls(u'Property Type'),
    )

    form.omitted('beds_baths')
    form.no_omit(configuration_view.IDefaultConfigureForm, 'beds_baths')
    form.widget(beds_baths='ps.plone.mlstiles.widgets.ListingTextFieldWidget')
    beds_baths = schema.TextLine(
        required=False,
        title=_mls(u'Beds/Baths'),
    )

    form.omitted('location')
    form.no_omit(configuration_view.IDefaultConfigureForm, 'location')
    form.widget(location='ps.plone.mlstiles.widgets.ListingTextFieldWidget')
    location = schema.TextLine(
        required=False,
        title=_mls(u'Location'),
    )

    form.omitted('location_type')
    form.no_omit(configuration_view.IDefaultConfigureForm, 'location_type')
    form.widget(
        location_type='ps.plone.mlstiles.widgets.ListingTextFieldWidget',
    )
    location_type = schema.TextLine(
        required=False,
        title=_mls(u'Location Type'),
    )

    form.omitted('view_type')
    form.no_omit(configuration_view.IDefaultConfigureForm, 'view_type')
    form.widget(view_type='ps.plone.mlstiles.widgets.ListingTextFieldWidget')
    view_type = schema.TextLine(
        required=False,
        title=_mls(u'View Type'),
    )

    form.omitted('lot_size')
    form.no_omit(configuration_view.IDefaultConfigureForm, 'lot_size')
    form.widget(lot_size='ps.plone.mlstiles.widgets.ListingTextFieldWidget')
    lot_size = schema.TextLine(
        required=False,
        title=_mls(u'Total Lot Size'),
    )

    footer = schema.TextLine(
        required=False,
        title=_cc(u'Footer'),
    )

    uuid = schema.TextLine(
        readonly=True,
        title=_cc(u'UUID'),
    )


@implementer(IListingCollectionTile)
class ListingCollectionTile(base.PersistentCoverTile):
    """A tile that shows a list of MLS listings."""

    is_configurable = True
    is_editable = True
    short_name = _(u'MLS: Listing Collection')
    index = ViewPageTemplateFile('collection.pt')
    configured_fields = []

    header = FieldProperty(IListingCollectionTile['header'])
    count = FieldProperty(IListingCollectionTile['count'])
    offset = FieldProperty(IListingCollectionTile['offset'])
    title = FieldProperty(IListingCollectionTile['title'])
    image = FieldProperty(IListingCollectionTile['image'])
    price = FieldProperty(IListingCollectionTile['price'])
    workflow_status = FieldProperty(IListingCollectionTile['workflow_status'])
    listing_type = FieldProperty(IListingCollectionTile['listing_type'])
    image_count = FieldProperty(IListingCollectionTile['image_count'])
    object_type = FieldProperty(IListingCollectionTile['object_type'])
    beds_baths = FieldProperty(IListingCollectionTile['beds_baths'])
    location = FieldProperty(IListingCollectionTile['location'])
    location_type = FieldProperty(IListingCollectionTile['location_type'])
    view_type = FieldProperty(IListingCollectionTile['view_type'])
    lot_size = FieldProperty(IListingCollectionTile['lot_size'])
    footer = FieldProperty(IListingCollectionTile['footer'])
    uuid = FieldProperty(IListingCollectionTile['uuid'])

    def get_title(self):
        return self.data['title']

    def has_listing_collection(self, obj):
        """Check if the obj is activated for recent MLS listings."""
        return listing_collection.IListingCollection.providedBy(obj)

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(listing_collection.CONFIGURATION_KEY, {})

    def results(self):
        items = []

        self.configured_fields = self.get_configured_fields()
        size_conf = [
            i for i in self.configured_fields if i['id'] == 'count'
        ]

        if size_conf and 'size' in size_conf[0].keys():
            size = int(size_conf[0]['size'])
        else:
            size = 5

        offset = 0
        offset_conf = [
            i for i in self.configured_fields if i['id'] == 'offset'
        ]
        if offset_conf:
            try:
                offset = int(offset_conf[0].get('offset', 0))
            except ValueError:
                offset = 0

        uuid = self.data.get('uuid', None)
        obj = uuidToObject(uuid)
        if uuid and obj:
            if not self.has_listing_collection(obj):
                return items
            config = copy.copy(self.get_config(obj))
            portal_state = obj.unrestrictedTraverse('@@plone_portal_state')
            params = {
                'limit': size,
                'offset': offset,
                'lang': portal_state.language(),
            }
            config.update(params)
            items = api.search(
                params=api.prepare_search_params(config),
                batching=False,
                context=obj,
            )
        else:
            self.remove_relation()

        return items

    def is_empty(self):
        return self.data.get('uuid', None) is None or \
            uuidToObject(self.data.get('uuid')) is None

    def populate_with_object(self, obj):
        # Check permission.
        super(ListingCollectionTile, self).populate_with_object(obj)

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

    def _field_wrapped_in_link(self, field):
        tile_conf = self.get_tile_configuration()
        field_conf = tile_conf.get(field, None)
        if field_conf and isinstance(field_conf, dict):
            return field_conf.get('wraplink', None) == u'on'
        else:
            return False

    def get_configured_fields(self):
        # Override this method, since we are not storing anything
        # in the fields, we just use them for configuration
        tileType = queryUtility(ITileType, name=self.__name__)
        conf = self.get_tile_configuration()

        fields = schema.getFieldsInOrder(tileType.schema)

        results = []
        for name, obj in fields:
            field = {'id': name,
                     'title': obj.title}
            if name in conf:
                field_conf = conf[name]
                if ('visibility' in field_conf and
                        field_conf['visibility'] == u'off'):
                    # If the field was configured to be invisible, then just
                    # ignore it
                    continue

                if 'htmltag' in field_conf:
                    # If this field has the capability to change its html tag
                    # render, save it here
                    field['htmltag'] = field_conf['htmltag']

                if 'htmltag-listings' in field_conf:
                    # If this field has the capability to change its html tag
                    # render, save it here
                    field['htmltag-listings'] = field_conf['htmltag-listings']

                if 'wraplink' in field_conf:
                    field['wraplink'] = self._field_wrapped_in_link(name)

                if 'imgsize' in field_conf:
                    field['scale'] = field_conf['imgsize']

                if 'size' in field_conf:
                    field['size'] = field_conf['size']

                if 'offset' in field_conf:
                    field['offset'] = field_conf['offset']

            results.append(field)

        return results

    def thumbnail(self, item):
        """Return a thumbnail of an image if the item has an image field and
        the field is visible in the tile.

        :param item: [required]
        :type item: content object
        """
        if self._has_image_field(item) and self._field_is_visible('image'):
            tile_conf = self.get_tile_configuration()
            image_conf = tile_conf.get('image', None)
            if image_conf:
                scaleconf = image_conf['imgsize']
                # Scale string is something like: 'mini 200:200'.
                # We need the name only: 'mini'.
                scale = scaleconf.split(' ')[0]
                scales = item.restrictedTraverse('@@images')
                return scales.scale('image', scale)

    @view.memoize
    def get_image_position(self):
        tile_conf = self.get_tile_configuration()
        image_conf = tile_conf.get('image', None)
        if image_conf:
            return image_conf['position']

    def remove_relation(self):
        data_mgr = ITileDataManager(self)
        old_data = data_mgr.get()
        if 'uuid' in old_data:
            old_data.pop('uuid')
        data_mgr.set(old_data)

    def show_header(self):
        return self._field_is_visible('header')

    def collection_url(self):
        uuid = self.data.get('uuid', None)
        obj = uuidToObject(uuid)
        return obj.absolute_url() if obj else ''

    def show_footer(self):
        return self._field_is_visible('footer')


@implementer(IListingCollectionTile)
class RecentListingsTile(ListingCollectionTile):
    """A tile that shows a list of recent MLS listings."""

    short_name = _(u'MLS: Recent Listings')

    def has_listing_collection(self, obj):
        """Check if the obj is activated for recent MLS listings."""
        return recent_listings.IRecentListings.providedBy(obj)

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(recent_listings.CONFIGURATION_KEY, {})


@implementer(IListingCollectionTile)
class FeaturedListingsTile(ListingCollectionTile):
    """A tile that shows a list of featured MLS listings."""

    short_name = _(u'MLS: Featured Listings')

    def has_listing_collection(self, obj):
        """Check if the obj is activated for recent MLS listings."""
        return featured.IFeaturedListings.providedBy(obj)

    def get_config(self, obj):
        """Get collection configuration data from annotations."""
        annotations = IAnnotations(obj)
        return annotations.get(featured.CONFIGURATION_KEY, {})
