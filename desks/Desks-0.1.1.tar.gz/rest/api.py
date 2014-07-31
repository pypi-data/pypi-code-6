#!/usr/bin/env python
import ConfigParser
import re
import os

from flask import Flask, current_app
from flask.ext import restful
from shelves.shelves import WhooshFileShelf
from shelves.boxes import FileBox

from resources.search import SearchResource
from resources.token import TokenResource
from resources.document import DocResource, mediaResource

app = Flask(__name__, instance_relative_config=True)
# Let's get application config
app.config.from_pyfile('config.py')

# Let's create shelves and the like
parser = ConfigParser.SafeConfigParser()
parser.read(app.config['DESK_CONFIG'])

if not parser.has_section('Shelf'):
    raise Exception("Incorrect configuration - Section Shelf missing")

shelf_type = globals()[parser.get('Shelf', 'Type')]
shelf = shelf_type(parser.get('Shelf', 'Path'))

for box_config in [box for box in parser.sections() for match in [re.search('Box', box)] if match]:
    box_type = parser.get(box_config, 'Type')
    if box_type == 'FileBox':
        shelf.boxes.append(FileBox(parser.get(box_config, 'Path')))

with app.app_context():
    current_app.shelf = shelf

# Now let's start the RESTfull Api
api = restful.Api(app)
api.add_resource(SearchResource, '/search/', '/search/<string:search_id>/', endpoint='search_ep')
api.add_resource(TokenResource, '/token/', endpoint='token_ep')
api.add_resource(DocResource, '/doc/', '/doc/<string:doc_id>/', endpoint='doc_ep')

app.add_url_rule('/media/<string:doc_id>', 'media_ep', mediaResource)

app.run(debug=True)
