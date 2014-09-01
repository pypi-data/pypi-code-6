import js.jquery
from fanstatic import Library, Resource, Group

library = Library('bootstrap-slider', 'resources')

slider_css = Resource(
    library, 'bootstrap-slider.css',
    minified='bootstrap-slider.min.css')

slider_js = Resource(
    library, 'bootstrap-slider.js',
    minified='bootstrap-slider.min.js',
    depends=[js.jquery.jquery])

slider = Group([slider_css, slider_js])
