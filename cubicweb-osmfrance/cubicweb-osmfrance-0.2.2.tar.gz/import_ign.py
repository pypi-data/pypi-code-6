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
$ cubicweb/bin/cubicweb-ctl ign_import_shp <myinstance> ...
(see the README file)

It can be also launched through the cubicweb shell, using default paths for the
input files, with:
$ cubicweb-ctl shell <myinstance> import_ign.py
"""

import os

from cubes.osmfrance import SRID_RGF93
from cubes.osmfrance.import_shp import _Collection
from cubes.osmfrance.nuts import COG_REGIONS_TO_NUTS, COG_DEPARTEMENTS_TO_NUTS


## caches
REGIONS = {}
DEPARTEMENTS = {}


def _get_geometry(prop):
    geom = prop.GetGeometryRef()
    return (geom.ExportToWkt(), SRID_RGF93)


def import_departements(session, filepath):
    with _Collection(filepath) as collection:
        for prop in collection:
            #['ID_GEOFLA', 'CODE_DEPT', 'NOM_DEPT', 'CODE_CHF', 'NOM_CHF',
            #'X_CHF_LIEU', 'Y_CHF_LIEU', 'X_CENTROID', 'Y_CENTROID', 'CODE_REG',
            #'NOM_REGION']
            code_r = prop['CODE_REG']
            if not code_r in REGIONS:
                region = session.create_entity('Region',
                                               name=prop['NOM_REGION'].title(),
                                               insee=code_r,
                                               nuts2=unicode(COG_REGIONS_TO_NUTS[code_r]))
                REGIONS[code_r] = region.eid

            code_d = prop['CODE_DEPT']
            dept = session.create_entity('Departement',
                                         name=prop['NOM_DEPT'].title(),
                                         insee=code_d,
                                         nuts3=unicode(COG_DEPARTEMENTS_TO_NUTS[code_d]),
                                         in_region=REGIONS[code_r],
                                         geometry=_get_geometry(prop),
                                         )
            DEPARTEMENTS[code_d] = dept.eid

def import_arrondissements(session, filepath):
    with _Collection(filepath) as collection:
        for prop in collection:
            #['ID_GEOFLA', 'CODE_ARR', 'CODE_CHF', 'NOM_CHF', 'X_CHF_LIEU',
            #'Y_CHF_LIEU', 'X_CENTROID', 'Y_CENTROID', 'CODE_DEPT', 'NOM_DEPT',
            #'CODE_REG', 'NOM_REGION']
            code_d = prop['CODE_DEPT']
            code_a = prop['CODE_ARR']
            arr = session.create_entity('Arrondissement',
                                        name=prop['NOM_CHF'].title(),
                                        insee=code_d+code_a,
                                        ar_in_departement=DEPARTEMENTS[code_d],
                                        geometry=_get_geometry(prop),
                                        )


def import_communes(session, filepath):
    with _Collection(filepath) as collection:
        for prop in collection:
            #['ID_GEOFLA', 'CODE_COMM', 'INSEE_COM', 'NOM_COMM', 'STATUT',
            #'X_CHF_LIEU', 'Y_CHF_LIEU', 'X_CENTROID', 'Y_CENTROID', 'Z_MOYEN',
            #'SUPERFICIE', 'POPULATION', 'CODE_CANT', 'CODE_ARR', 'CODE_DEPT',
            #'NOM_DEPT', 'CODE_REG', 'NOM_REGION']
            code_d = prop['CODE_DEPT']

            session.create_entity('Commune',
                                  name=prop['NOM_COMM'].title(),
                                  insee=prop['INSEE_COM'],
                                  area=float(prop['SUPERFICIE'])/100.,
                                  in_departement=DEPARTEMENTS[code_d],
                                  geometry=_get_geometry(prop),
                                  )


if __name__ == '__main__':
    geodir = "GEOFLA_1-1_SHP_LAMB93_FR-ED131"
    datadirpath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data',
                               geodir, "GEOFLA")
    ign_files = {'departements': os.path.join(datadirpath,
        "1_DONNEES_LIVRAISON_2013-11-00162", geodir, "DEPARTEMENTS",
        "DEPARTEMENT.SHP"),
                 'arrondissements': os.path.join(datadirpath,
        "1_DONNEES_LIVRAISON_2013-11-00164", geodir, "ARRONDISSEMENTS",
        "ARRONDISSEMENT.SHP"),
                 'cantons': os.path.join(datadirpath,
        "1_DONNEES_LIVRAISON_2013-11-00163", geodir, "CANTONS",
        "CANTON.SHP"),
                 'communes': os.path.join(datadirpath,
        "1_DONNEES_LIVRAISON_2013-11-00161", geodir, "COMMUNES",
        "COMMUNE.SHP"),
            }
    print "Import regions and departements"
    import_departements(session, ign_files['departements'])

    print "Import arrondissements"
    import_arrondissements(session, ign_files['arrondissements'])

    print "Import communes"
    import_communes(session, ign_files['communes'])

    print "Import finished"
