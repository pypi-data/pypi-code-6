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

"""cubicweb-clinipath schema"""

from yams.buildobjs import (EntityType, SubjectRelation, String, RichString, Int, Date)


class Biopsy(EntityType):
    """Biopsy attributes"""
    biopsy_type = String(maxsize=512)
    extraction_date = Datetime()
    size = String(maxsize=128)
    tumoral_cell_percent = Float(indexed=True)
    necrosis_percent = Float(indexed=True)
    has_gene_expression = Boolean()
    proliferating_cell_percent = Float()
    has_neoangiogenesis = Boolean()
    has_necrosis = Boolean()
    conclusions = String(maxsize=2056, fulltextindexed=True)


class BiopsySample(EntityType):
    size = String(maxsize=128)
    tumoral_cell_percent = Float(indexed=True)
    necrosis_percent = Float(indexed=True)
    has_gene_expression = Boolean()
    proliferating_cell_percent = Float()
    has_neoangiogenesis = Boolean()
    has_necrosis = Boolean()
    extracted_from = SubjectRelation('Biopsy', cardinality='1*', inlined=True)


class CellCulture(EntityType):
    """ Models cell cultures, with passages for now. Related to a
    Biopsy."""
    code = Int()
    culture_passage = Int()
    related_biopsy = SubjectRelation('Biopsy', cardinality='?*',
                                     inlined=True, composite='object')


class BloodSample(EntityType):
    """ Blood sample data """
    code = Int(required=True)
    volume_ml = Int()
    sampling_date = Date()


class IHCMeasure(EntityType):
    """An IHC measure."""
    measured_on = SubjectRelation(('Biopsy', 'CellCulture'), inlined=True, cardinality='1*')


class IHCResult(EntityType):
    """ An IHC result."""
    expression_value = Int(indexed=True)
    related_measure = SubjectRelation('IHCMeasure', inlined=True, cardinality='1*')


class AnatomicPathologyReport(EntityType):
    """ An Anatomic pathology report """
    code = Int(required=True)
    description = RichString(fulltextindexed=True)
    conclusions = RichString(fulltextindexed=True)
    report_on = SubjectRelation(('Biopsy', 'CellCulture', 'BloodSample'),
                                inlined=True, cardinality='1*', composite='object')
