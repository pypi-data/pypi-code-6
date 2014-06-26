"""cubicweb-vtimeline views/forms/actions/components for web ui"""
import json
from itertools import chain

from logilab.common.date import ustrftime

from cubicweb.predicates import is_instance

try:
    from cubes.vtimeline.views import VeriteCoTimelineJsonDataView, VeriteCoTimelineView
except ImportError:
    pass
else:
    class SubjectVeriteCoTimelineView(VeriteCoTimelineView):
        __regid__ = 'vtimeline'
        __select__ = is_instance('Subject')


    class VeriteCoTimelineJsonDataView(VeriteCoTimelineJsonDataView):
        __select__ = is_instance('Subject')

        def call(self):
            dates = []
            d = {'timeline': {'headline': '', 'type': 'default', 'text': '', 'date': dates}}
            for entity in self.cw_rset.entities():
                # Subject dates
                for admission in entity.reverse_admission_of:
                    study = admission.admission_in[0]
                    for date, label in ((admission.admission_date, self._cw._('Admission in')),
                                        (admission.admission_end_date, self._cw._('Out of'))):
                        if not date:
                            continue
                        text = u'<p>%s - %s</p>' % (label, study.view('incontext'))
                        dates.append({'startDate': ustrftime(date, '%Y,%m,%d'),
                                      'headline': label,
                                      'text': text})
                    # Steps
                    for step in admission.reverse_step_of:
                        if step.step_date:
                            dates.append({'startDate': ustrftime(step.step_date, '%Y,%m,%d'),
                                          'headline': step.name,
                                          'text': u'<p>%s</p>' % study.view('incontext')})
                # Measures
                for measure in entity.reverse_concerns:
                    calendarable = measure.cw_adapt_to('ICalendarable')
                    # Measure adapter
                    if calendarable and calendarable.start:
                        dates.append({'startDate': ustrftime(calendarable.start, '%Y,%m,%d'),
                                      'headline': measure.view('incontext')})
                    # Fallback to assessment
                    elif measure.reverse_generates:
                        calendarable = measure.reverse_generates[0].cw_adapt_to('ICalendarable')
                        if calendarable and calendarable.start:
                            dates.append({'startDate': ustrftime(calendarable.start, '%Y,%m,%d'),
                                          'headline': measure.view('incontext')})
                # Diagnostics/Therapies
                for e in chain(entity.related_diagnostics, entity.related_therapies):
                    calendarable = e.cw_adapt_to('ICalendarable')
                    # Measure adapter
                    if calendarable and calendarable.start:
                        dates.append({'startDate': ustrftime(calendarable.start, '%Y,%m,%d'),
                                      'headline': e.view('incontext')})
                    # Drugtake
                    if e.cw_etype == 'Therapy':
                        for drugtake in e.reverse_taken_in_therapy:
                            date = drugtake.start_taking_date
                            if date:
                                dates.append({'startDate': ustrftime(date, '%Y,%m,%d'),
                                              'headline': drugtake.view('incontext')})
            self.w(json.dumps(d))


    def registration_callback(vreg):
        vreg.register(VeriteCoTimelineJsonDataView)
        vreg.register_and_replace(SubjectVeriteCoTimelineView, VeriteCoTimelineView)
