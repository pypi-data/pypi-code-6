from django_assets import Bundle, register

def standard_bundle(name, source):
    bundle = Bundle('js/jquip/src/%s.js' % source,
        filters=['jsmin'],
        output='js/pyquip/%s.min.js' % source)
    register('jquip.%s' % name, bundle)
    return bundle

core = standard_bundle('core', 'jquip')
ajax = standard_bundle('ajax', 'jquip.ajax')
css  = standard_bundle('css', 'jquip.css')
custom = standard_bundle('custom', 'jquip.custom')
docready = standard_bundle('docready', 'jquip.docready')
events = standard_bundle('events', 'jquip.events')
q_min = standard_bundle('q_min', 'jquip.q-min')

all = Bundle(core, ajax, css, custom, docready, events, q_min,
    output='js/pyquip/jquip.all.min.js')
