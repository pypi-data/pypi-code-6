import json
from flask import Blueprint
from flask import jsonify
from flask.ext.cors import cross_origin
from flask import request
from flask import Response
from pgeo.error.custom_exceptions import PGeoException
from pgeo.thread.download_threads_manager import Manager
from pgeo.thread.download_threads_manager import progress_map
from pgeo.thread.download_threads_manager import out_template


download = Blueprint('download', __name__)


@download.route('/')
def index():
    return 'Welcome to the Download module!'

@download.route('/<source_name>', methods=['POST'])
@download.route('/<source_name>/', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def manager_start(source_name):
    try:
        payload = request.get_json()
        file_paths_and_sizes = payload['file_paths_and_sizes']
        filesystem_structure = payload['filesystem_structure']
        mgr = Manager(source_name, file_paths_and_sizes, filesystem_structure)
        mgr.run()
        return Response(json.dumps('Manager started.'), content_type='application/json; charset=utf-8')
    except Exception, e:
        raise PGeoException(e.message, 500)


@download.route('/progress/<layer_name>')
@download.route('/progress/<layer_name>/')
@cross_origin(origins='*')
def progress(layer_name):
    if layer_name not in progress_map:
        return jsonify(progress=out_template)
    return jsonify(progress_map[layer_name])