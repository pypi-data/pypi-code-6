import json
from flask import Blueprint
from flask import jsonify
from flask.ext.cors import cross_origin
from flask import request
from flask import Response
from pgeo.error.custom_exceptions import PGeoException
from pgeo.thread.download_threads_manager import Manager
from pgeo.thread.bulk_download_threads_manager import BulkDownloadManager
from pgeo.thread.bulk_download_threads_manager import progress_map as bulk_progress_map
from pgeo.thread.download_threads_manager import multi_progress_map
from pgeo.thread.download_threads_manager import out_template
from pgeo.gis.raster import process_hdfs
from pgeo.config.settings import read_config_file_json


download = Blueprint('download', __name__)
managers = {}


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
        tab_id = payload['tab_id']
        if tab_id not in managers:
            managers[tab_id] = {}
        mgr = Manager(source_name, file_paths_and_sizes, filesystem_structure, tab_id)
        target_dir = mgr.run()
        out = {'source_path': target_dir}
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except Exception, e:
        print e
        raise PGeoException(e.message, 500)


@download.route('/progress/<tab_index>/<layer_name>')
@download.route('/progress/<tab_index>/<layer_name>/')
@cross_origin(origins='*')
def multiple_progress(layer_name, tab_index):
    if tab_index not in multi_progress_map:
        return jsonify(progress=out_template)
    if layer_name not in multi_progress_map[tab_index]:
        return jsonify(progress=out_template)
    return jsonify(multi_progress_map[tab_index][layer_name])


@download.route('/process/<source_name>', methods=['POST'])
@download.route('/process/<source_name>/', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def process_rasters_service(source_name):
    try:
        payload = request.get_json()
        conf = read_config_file_json(source_name, 'data_providers')
        obj = conf['processing']
        obj['source_path'] = payload['source_path']
        obj['output_path'] = payload['source_path'] + '/OUTPUT'
        obj['gdalwarp']['-tr'] = str(payload['pixel_size']) + ', -' + str(payload['pixel_size'])
        try:
            tiff = process_hdfs(obj)
            return Response(json.dumps('{"TIFF":"' + tiff + '"}'), content_type='application/json; charset=utf-8')
        except Exception, e:
            return Response(json.dumps('{"Message":"' + e.message + '"}'), content_type='application/json; charset=utf-8')
    except Exception, e:
        return Response(json.dumps('{"Message":"' + e.message + '"}'), content_type='application/json; charset=utf-8')


@download.route('/bulk/<source_name>', methods=['POST'])
@download.route('/bulk/<source_name>/', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def bulk_manager_start(source_name):
    try:
        payload = request.get_json()
        filesystem_structure = payload['filesystem_structure']
        bulk_download_objects = payload['bulk_download_objects']
        tab_id = payload['tab_id']
        mgr = BulkDownloadManager(source_name, filesystem_structure, bulk_download_objects, tab_id)
        target_dir = mgr.run()
        out = {'source_path': target_dir}
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except Exception, e:
        raise PGeoException(e.message, 500)


@download.route('/bulk/progress/<tab_index>')
@download.route('/bulk/progress/<tab_index>/')
@cross_origin(origins='*')
def bulk_progress(tab_index):
    if tab_index not in bulk_progress_map:
        return jsonify(progress=out_template)
    status = bulk_progress_map[tab_index]['status']
    print bulk_progress_map[tab_index]
    if 'ERROR' in status:
        raise PGeoException(status, 500)
    if 'COMPLETE' in status:
        raise PGeoException(status, 500)
    return jsonify(bulk_progress_map[tab_index])