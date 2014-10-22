from fanstatic import Library, Resource
import js.jquery

library = Library('jquery_numeric', 'resources')

numeric = Resource(
    library, 'jquery.numeric.js',
    minified='jquery.numeric.min.js',
    depends=[js.jquery.jquery])
