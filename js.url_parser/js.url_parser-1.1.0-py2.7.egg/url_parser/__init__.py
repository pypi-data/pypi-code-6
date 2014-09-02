from fanstatic import Library, Resource

library = Library('url-parser', 'resources')

url_parser = Resource(library, 'url-parser.js',
                      minified='url-parser.min.js',
                      bottom=True)
