# -*- coding: utf8 -*-
from __future__ import unicode_literals

from django.contrib.admin import ModelAdmin

try:
    from djgeojson.fields import GeoJSONField
except ImportError:
    GeoJSONField = type(object)
try:
    from django.contrib.gis.db.models import GeometryField
    from .forms.widgets import LeafletWidget
except ImportError:
    GeometryField = type(object)
    from django.forms.widgets import Textarea as LeafletWidget


class LeafletGeoAdmin(ModelAdmin):
    widget = LeafletWidget
    map_template = 'leaflet/admin/widget.html'
    modifiable = True
    map_width = '100%'
    map_height = '400px'
    display_raw = False

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Overloaded from ModelAdmin to set Leaflet widget
        in form field init params.
        """
        is_geometry = isinstance(db_field, (GeometryField, GeoJSONField))
        is_editable = is_geometry and (db_field.dim < 3 or
                                       self.widget.supports_3d)

        if is_editable:
            kwargs.pop('request', None)  # unsupported for form field
            # Setting the widget with the newly defined widget.
            kwargs['widget'] = self._get_map_widget(db_field)
            return db_field.formfield(**kwargs)
        else:
            return super(LeafletGeoAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def _get_map_widget(self, db_field):
        """
        Overriden LeafletWidget with LeafletGeoAdmin params.
        """
        class LeafletMap(self.widget):
            template_name = self.map_template
            include_media = True
            geom_type = db_field.geom_type
            modifiable = self.modifiable
            map_width = self.map_width
            map_height = self.map_height
            display_raw = self.display_raw
        return LeafletMap
