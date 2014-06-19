from js.jquery import jquery
from js.jqueryui import jqueryui
import fanstatic


library = fanstatic.Library('ehynds_multiselect', 'resources')


multiselect_css = fanstatic.Resource(
    library, 'jquery.multiselect.css', minified='jquery.multiselect.min.css')
multiselect = fanstatic.Resource(
    library, 'jquery.multiselect.js', minified='jquery.multiselect.min.js',
    depends=[jquery, jqueryui, multiselect_css])
