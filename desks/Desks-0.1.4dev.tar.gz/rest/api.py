#!/usr/bin/env python
import ConfigParser
import re
import os
import random
import string
import json
from hashlib import sha1, sha256

from flask import Flask, current_app
from flask.ext import restful
from shelves.shelves.file import FileShelf
from shelves.boxes.file import FileBox

from resources.search import SearchResource
from resources.token import TokenResource
from resources.document import DocResource, mediaResource
from resources.schema import SchemaResource

def config():
    """
    This method is used to generate the config.py instance script.
    """
    app = Flask(__name__, instance_relative_config=True)
    config = {}
    config['DEBUG'] = True
    config['PRIVATE_KEY'] = '.'.join([sha1(str(random.random())).hexdigest()
                                    , sha1(str(random.random())).hexdigest()])
    config['TOKEN_LIST'] = os.path.join(app.instance_path, 'token.json')
    config['DESK_CONFIG'] = os.path.join(app.instance_path, 'desk.ini')
    config['TEMP_UPLOAD_DIR'] = os.path.join(os.getenv('TEMPDIR', os.getenv('TEMP', os.getenv('TMP', './tmp'))), 'desk')

    # Let's load the default
    app.config.from_object(__name__)
    app.config.update(config)
    config_file = os.path.join(app.instance_path, 'config.py')
    # Let's try to load the config file if it exist
    # it will overwite our defaults
    app.config.from_pyfile('config.py', silent=True)
    if not os.path.isfile(config_file):
        # Config file does not exist this will create it
        os.path.isdir(os.path.dirname(config_file)) or os.makedirs(os.path.dirname(config_file))
        open(config_file, 'w').close()

    # Now, let's write our file
    with open(config_file, 'w') as conf:
        for key in config:
            conf.write("%s = %s\n" % (key, repr(app.config[key])))

    # We need to create a first token
    if not os.path.isfile(app.config['TOKEN_LIST']):
        with open(app.config['TOKEN_LIST'], 'w') as tkl:
            token = ''.join([string.ascii_letters[random.randint(0, len(string.ascii_letters) - 1)] for x in xrange(20)])
            print("We've randomly created a token for you, keep it safe: %s" % token)
            json.dump([token], tkl)

def run():
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
    api.add_resource(SchemaResource, '/schema/', endpoint='schema_ep')

    app.add_url_rule('/media/<string:doc_id>', 'media_ep', mediaResource)

    app.run(debug=app.config['DEBUG'])

if __name__ == "__main__":
    run()
