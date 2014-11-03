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

"""
This script cannot be run directly. It is called by the ccplugin script:
$ cubicweb/bin/cubicweb-ctl osmfrance_import_shp <myinstance> ...
(see the README file)

It can be also launched through the cubicweb shell, using default paths for the
input files, with:
$ cubicweb-ctl shell <myinstance> import_osm.py
"""

import os
from osgeo import ogr

from cubes.osmfrance.import_shp import _Collection
from cubes.osmfrance import SRID_WGS84


## cache for associating communes, departements and regions
REGIONS = {}
DEPARTEMENTS = {}


def _get_geometry(prop):
    geom = prop.GetGeometryRef()
    return (ogr.ForceToMultiPolygon(geom).ExportToWkt(), SRID_WGS84)


def import_regions(session, filepath):
    with _Collection(filepath) as collection:
        for prop in collection:
            name = prop['nom']

            regentity = session.create_entity('Region',
                                              name=name,
                                              insee=prop['code_insee'],
                                              chef_lieu_name=prop['nom_cl'],
                                              chef_lieu_insee=prop['insee_cl'],
                                              nuts2=prop['nuts2'],
                                              nb_dep=int(prop['nb_dep']),
                                              nb_comm=int(prop['nb_comm']),
                                              area=float(prop['surf_km2']),
                                              geometry=_get_geometry(prop)
                                              )
            REGIONS[prop['nuts2']] = regentity.eid


def import_departements(session, filepath):
    with _Collection(filepath) as collection:
        for prop in collection:
            name = prop['nom']

            ## The first 4 characters of NUTS3 (departement) [e.g. FR10x]
            ## is the enclosing region NUTS2 code [e.g. FR10]
            region_eid = REGIONS[prop['nuts3'][:4]]

            dept = session.create_entity('Departement',
                                         name=name,
                                         insee=prop['code_insee'],
                                         nuts3=prop['nuts3'],
                                         in_region=region_eid,
                                         geometry=_get_geometry(prop),
                                         )
            DEPARTEMENTS[prop['code_insee']] = dept.eid


def import_arrondissements(session, filepath):
    with _Collection(filepath) as collection:
        for prop in collection:
            name = prop['nom']
            dept_eid = DEPARTEMENTS[prop['insee_ar'][:-1]]

            session.create_entity('Arrondissement',
                                  name=name,
                                  insee=prop['insee_ar'],
                                  nb_comm=int(prop['nb_comm']),
                                  area=float(prop['surf_km2']),
                                  ar_in_departement=dept_eid,
                                  geometry=_get_geometry(prop)
                                  )


def import_epci(session, filepath):
    with _Collection(filepath) as collection:
        for prop in collection:
            name = prop['nom_epci']

            session.create_entity('Epci',
                                  name=name,
                                  code=prop['siren_epci'],
                                  population=int(prop['ptot_epci']),
                                  area=float(prop['surf_km2']),
                                  geometry=_get_geometry(prop)
                                  )


def import_communes(session, filepath):

    with _Collection(filepath) as collection:
        for prop in collection:
            name = prop['nom']

            ## The first 2 (3 for DOM) characters of the insee code for communes
            ## is the enclosing departement insee code
            insee = prop['insee']
            dept_insee = insee[:3] if insee.startswith('97') else insee[:2]
            dept_eid = DEPARTEMENTS[dept_insee]

            session.create_entity('Commune',
                                  name=name,
                                  insee=prop['insee'],
                                  area=float(prop['surf_m2'])/1e6,
                                  in_departement=dept_eid,
                                  geometry=_get_geometry(prop)
                                  )


if __name__ == '__main__':
    datadirpath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
    osmfrance_files = {'regions': "regions-20140306-50m.shp",
                       'departements': "departements-20140306-100m.shp",
                       'epci': "epci-20140306-100m.shp",
                       'communes': "communes-20140306-100m.shp",
                       'arrondissements': "arrondissements-20131220-100m.shp"
                       }

    print "Import regions"
    import_regions(session, os.path.join(datadirpath, osmfrance_files['regions']))
    print "Import departements"
    import_departements(session, os.path.join(datadirpath, osmfrance_files['departements']))
    print "Import arrondissements"
    import_arrondissements(session, os.path.join(datadirpath, osmfrance_files['arrondissements']))
    print "Import epci"
    import_epci(session, os.path.join(datadirpath, osmfrance_files['epci']))
    print "Import communes"
    import_communes(session, os.path.join(datadirpath, osmfrance_files['communes']))
    print "Import finished"
