# -*- coding: utf-8 -*-
# copyright 2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-osmfrance views/forms/actions/components for web ui"""

from cubicweb.utils import js_dumps, JSString
from cubicweb.predicates import is_instance
from cubicweb.web.views import uicfg
from cubes.leaflet import views

_pvs = uicfg.primaryview_section

# hide Geometry (type str, CW needs it as unicode to display)
_pvs.tag_attribute(('Region', 'geometry'), 'hidden')
_pvs.tag_attribute(('Departement', 'geometry'), 'hidden')
_pvs.tag_attribute(('Arrondissement', 'geometry'), 'hidden')
_pvs.tag_attribute(('Epci', 'geometry'), 'hidden')
_pvs.tag_attribute(('Commune', 'geometry'), 'hidden')

views.LeafletMap.default_settings.update({'height': '900px',
                                          'maxZoom': 20,
                                          'minZoom': 5,
                                          'initialZoom': 10,
                                          'provider': 'esri-topomap',})

class GeoJsonView(views.GeoJsonView):
    '''same as cubes.leaflet.vies.GeoJsonView but allow to pass
    a 'Region', 'Departement', 'Arrondissement', 'Epci' or 'Commune'.
    '''
    __select__ = (views.GeoJsonView.__select__ &
                  is_instance('Region', 'Departement', 'Arrondissement',
                              'Epci', 'Commune'))

    def _get_geo(self, row):
        return self._cw.execute('Any DISPLAY(G, 4326) WHERE X eid %(eid)s, '
                                '                     X geometry G',
                                {'eid': row[0]})[0][0]

    def build_markers(self, *args, **kwargs):
        """ Build the markers from an rset """
        return JSString('[%s]' % ', '.join(
            self._get_geo(row) for row in self.cw_rset.rows))


class GeoJsonValuesView(views.GeoJsonValuesView):
    '''same as cubes.leaflet.vies.GeoJsonValuesView but allow to pass
    a 'Region', 'Departement', 'Arrondissement', 'Epci' or 'Commune'
    in the first column.
    '''
    __select__ = (views.GeoJsonValuesView.__select__ &
                  is_instance('Region', 'Departement', 'Arrondissement',
                              'Epci', 'Commune'))

    def _get_geo(self, row):
        return self._cw.execute('Any DISPLAY(G, 4326) WHERE X eid %(eid)s, '
                                '                     X geometry G',
                                {'eid': row[0]})[0][0]

    def build_markers(self, *args, **kwargs):
        # workaround on cubicweb-postgis bug which return a character
        # string instead of a JSString
        out = super(GeoJsonValuesView, self).build_markers(*args, **kwargs)
        if isinstance(out, JSString):
            return out
        return JSString(out)


