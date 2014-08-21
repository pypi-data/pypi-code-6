from flask import Flask
from flask.ext.cors import CORS

from pgeorest.browse_modis import browse_modis
from pgeorest.download import download
from pgeorest.browse_trmm import browse_trmm
from pgeorest.schema import schema
from pgeorest.filesystem import filesystem
from pgeorest.metadata import metadata
from pgeorest.search import search
from pgeorest import stats

import logging


app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(browse_modis, url_prefix='/browse/modis')
app.register_blueprint(browse_trmm, url_prefix='/browse/trmm')
app.register_blueprint(download, url_prefix='/download')
app.register_blueprint(schema, url_prefix='/schema')
app.register_blueprint(filesystem, url_prefix='/filesystem')
app.register_blueprint(stats.app, url_prefix='/stats')
app.register_blueprint(metadata, url_prefix='/metadata')
app.register_blueprint(search, url_prefix='/search')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)