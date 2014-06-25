# -*- coding: utf-8 -*-
# copyright 2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# copyright 2013 CEA (Saclay, FRANCE), all rights reserved.
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

"""cubicweb-medicalexp views/forms/actions/components for web ui"""

from cubicweb.web import facet
from cubicweb.predicates import is_instance

class SubjectGenderFacet(facet.AttributeFacet):
    __regid__ = 'subject-gender-facet'
    __select__ = facet.AttributeFacet.__select__ & is_instance('Subject')
    order = 1
    rtype = 'gender'
    title = _('Gender')


class SubjectHandednessFacet(facet.AttributeFacet):
    __regid__ = 'subject-handedness-facet'
    __select__ = facet.AttributeFacet.__select__ & is_instance('Subject')
    order = 2
    rtype = 'handedness'
    title = _('Handedness')


class SubjectStudyFacet(facet.RelationFacet):
    __regid__ = 'subject-study-facet'
    __select__ = facet.RelationFacet.__select__ & is_instance('Subject')
    order = 4
    rtype = 'related_studies'
    target_attr = 'name'
    title = _('Studies')


class TherapyStartDateFacet(facet.DateRangeFacet):
    __regid__ = 'therapy-start-date'
    __select__ = is_instance('Therapy')
    rtype = 'start_date'
    title = _('start_date')


class TherapyStopDateFacet(facet.DateRangeFacet):
    __regid__ = 'therapy-stop-date'
    __select__ = is_instance('Therapy')
    rtype = 'stop_date'
    title = _('stop_date')


class TherapyForFacet(facet.RelationFacet):
    __regid__ = 'therapy-for'
    __select__ = facet.RelationFacet.__select__ & is_instance('Therapy')
    rtype = 'therapy_for'
    target_attr = 'name'
    title = _('therapy_for')


class DiseaseLesionFacet(facet.RelationFacet):
    __regid__ = 'disease-lesion'
    __select__ = facet.RelationFacet.__select__ & is_instance('Disease')
    rtype = 'lesion_of'
    target_attr = 'name'
    title = _('lesion_of')


class DrugTakeDrug(facet.RelationFacet):
    __regid__ = 'drugtake-drug-facet'
    __select__ = facet.RelationFacet.__select__ & is_instance('DrugTake')
    rtype = 'drug'
    target_attr = 'name'
    title = _('drug')
    order = 2


class DrugStartDateFacet(facet.DateRangeFacet):
    __regid__ = 'drugtake-start-date'
    __select__ = is_instance('DrugTake')
    rtype = 'start_taking_date'
    title = _('start_taking_date')
    order = 7


class DrugStopDateFacet(facet.DateRangeFacet):
    __regid__ = 'drugtake-stop-date'
    __select__ = is_instance('DrugTake')
    rtype = 'stop_taking_date'
    title = _('stop_taking_date')
    order = 8


class DrugTakeDosis(facet.RangeFacet):
    __regid__ = 'drugtake-dosis-facet'
    __select__ = facet.RangeFacet.__select__ & is_instance('DrugTake')
    rtype = 'dosis'
    title = _('dosis')
    order = 4


class DrugTakeNumberOfCycles(facet.RangeFacet):
    __regid__ = 'drugtake-number_of_cycles-facet'
    __select__ = facet.RangeFacet.__select__ & is_instance('DrugTake')
    rtype = 'number_of_cycles'
    title = _('number_of_cycles')
    order = 3


class DrugTakeDosisPercentage(facet.RangeFacet):
    __regid__ = 'drugtake-dosis_percentage-facet'
    __select__ = facet.RangeFacet.__select__ & is_instance('DrugTake')
    rtype = 'dosis_percentage'
    title = _('dosis_percentage')
    order = 5


class DrugTakeUnits(facet.AttributeFacet):
    __regid__ = 'drugtake-units-facet'
    __select__ = facet.RangeFacet.__select__ & is_instance('DrugTake')
    rtype = 'unit'
    title = _('unit')
    order = 6


class DrugTakeReducedDosis(facet.AttributeFacet):
    __regid__ = 'drugtake-reduced_dosis-facet'
    __select__ = facet.RangeFacet.__select__ & is_instance('DrugTake')
    rtype = 'reduced_dosis'
    title = _('reduced_dosis')
    order = 9


class DiagnosticDatetimeFacet(facet.DateRangeFacet):
    __regid__ = 'diagnostic-datetime'
    __select__ = is_instance('Diagnostic')
    rtype = 'diagnostic_date'
    title = _('diagnostic_date')


class DiagnosticLocationFacet(facet.RelationFacet):
    __regid__ = 'diagnostic-location'
    __select__ = is_instance('Diagnostic')
    rtype = 'diagnostic_location'
    role = 'subject'
    target_attr = 'name'
    title = _('BodyLocation')


class DiagnosticDiseaseFacet(facet.RelationFacet):
    __regid__ = 'diagnostic-lesion'
    __select__ = is_instance('Diagnostic')
    rtype = 'diagnosed_disease'
    role = 'subject'
    target_attr = 'name'
    title = _('Disease')


class DiagnosticTechniqueFacet(facet.RelationFacet):
    __regid__ = 'diagnostic-technique'
    __select__ = is_instance('Diagnostic')
    rtype = 'technique_type'
    role = 'subject'
    target_attr = 'name'
    title = _('MedicalTechnique')



def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__, ())
    # Unregister unused/time-consuming facets
    from cubicweb.web.views.facets import (CWSourceFacet, CreatedByFacet,
                                           HasTextFacet, InGroupFacet, InStateFacet)
    vreg.unregister(CWSourceFacet)
    vreg.unregister(CreatedByFacet)
    vreg.unregister(InGroupFacet)
    vreg.unregister(InStateFacet)
    vreg.unregister(HasTextFacet)
