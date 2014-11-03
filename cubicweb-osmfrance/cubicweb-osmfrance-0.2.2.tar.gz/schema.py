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

"""cubicweb-osmfrance schema"""

from yams.buildobjs import (EntityType, Int, Float, String,
                            SubjectRelation, RelationDefinition)

from cubes.postgis.schema import Geometry
from cubes.osmfrance import SRID_WGS84


class Region(EntityType):

    name = String(fulltextindexed=True, unique=True, maxsize=30)
    insee = String(maxsize=2, required=True)
    chef_lieu_name = String(maxsize=30)
    chef_lieu_insee = String(maxsize=5)
    nuts2 = String(maxsize=4)
    nb_dep = Int()
    nb_comm = Int()
    area = Float()
    geometry = Geometry(geom_type='MULTIPOLYGON', srid=SRID_WGS84, coord_dimension=2)


class Departement(EntityType):

    name = String(fulltextindexed=True, unique=True, maxsize=30)
    insee = String(maxsize=3, required=True)
    nuts3 = String(maxsize=5)
    geometry = Geometry(geom_type='MULTIPOLYGON', srid=SRID_WGS84, coord_dimension=2)


class Arrondissement(EntityType):

    name = String(fulltextindexed=True, maxsize=50)
    insee = String(maxsize=4, required=True)
    nb_comm = Int()
    area = Float()
    geometry = Geometry(geom_type='MULTIPOLYGON', srid=SRID_WGS84, coord_dimension=2)


class Epci(EntityType):
    name = String(fulltextindexed=True)
    code = String(required=True)
    population = Int()
    area = Float()
    type_epci = String()
    geometry = Geometry(geom_type='MULTIPOLYGON', srid=SRID_WGS84, coord_dimension=2)


class Commune(EntityType):

    name = String(fulltextindexed=True, maxsize=50)
    insee = String(maxsize=7, required=True)
    area = Float()
    geometry = Geometry(geom_type='MULTIPOLYGON', srid=SRID_WGS84, coord_dimension=2)


class in_departement(RelationDefinition):
    subject = 'Commune'
    object = 'Departement'
    cardinality = '1*'
    inlined = True


class in_region(RelationDefinition):
    subject = 'Departement'
    object = 'Region'
    cardinality = '1*'
    inlined = True


class ar_in_departement(RelationDefinition):
    subject = 'Arrondissement'
    object = 'Departement'
    cardinality = '1*'
    inlined = True
