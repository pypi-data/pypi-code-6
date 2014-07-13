# -*- coding: utf-8 -*-

from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.cover.tiles.collection import CollectionTile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class CollectionTile(CollectionTile):
    """Class for custom template"""
    index = ViewPageTemplateFile('templates/tiles_collection.pt')

    def thumbnail(self, item):
        """Return a thumbnail of an image if the item has an image field and
        the field is visible in the tile.

        :param item: [required]
        :type item: content object
        """

        if self._has_image_field(item) and self._field_is_visible('image'):
            tile_conf = self.get_tile_configuration()
            image_conf = tile_conf.get('image', None)
            if not image_conf:
                return
            scaleconf = image_conf['imgsize']
            # scale string is something like: 'mini 200:200'
            # we need the name only: 'mini'
            if scaleconf == '_original':
                scale = None
            else:
                scale = scaleconf.split(' ')[0]

            if self._has_leadimage(item):
                """return the lead image tag"""
                field = item.getField(IMAGE_FIELD_NAME)
                if field is not None and field.get_size(item) != 0:
                    return field.tag(item, scale=scale, css_class='leadimage')

            else:
                scales = item.restrictedTraverse('@@images')
                return scales.scale('image', scale)

    def leadimage(self, item):
        """return lead image"""
        if self._has_leadimage(item) and self._field_is_visible('image'):
            tile_conf = self.get_tile_configuration()
            image_conf = tile_conf.get('image', None)
            if image_conf:
                scaleconf = image_conf['imgsize']
                # scale string is something like: 'mini 200:200'
                # we need the name only: 'mini'
                if scaleconf == '_original':
                    scale = None
                else:
                    scale = scaleconf.split(' ')[0]
            else:
                scale = None

            field = item.getField(IMAGE_FIELD_NAME)

            if field is not None and field.get_size(item) != 0:
                return field.tag(item, scale=scale, css_class='leadimage')
            else:
                return False
        else:
            return False

    def _has_image_field(self, item):
        """Return True if the object has an image field.

        :param obj: [required]
        :type obj: content object
        """

        if hasattr(item, 'image'):  # Dexterity
            return True
        elif hasattr(item, 'Schema'):  # Archetypes
            return 'image' in item.Schema().keys()
        else:
            return False

    def _has_leadimage(self, item):
        """Check for content Leadimage of an object"""

        field = item.getField(IMAGE_FIELD_NAME)
        if field is not None and field.get_size(item) != 0:
            return True
        else:
            return False
