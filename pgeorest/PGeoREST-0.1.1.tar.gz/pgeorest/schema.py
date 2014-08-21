import json
from flask import Blueprint
from flask import Response
from flask.ext.cors import cross_origin
from pgeo.error.custom_exceptions import PGeoException
from pgeo.error.custom_exceptions import errors
from pgeo.config.settings import read_config_file_json
from pgeo.utils.filesystem import list_sources

schema = Blueprint('schema', __name__)


@schema.route('/')
@cross_origin(origins='*')
def index():
    return 'Welcome to the Schema module!'


@schema.route('/sources', methods=['GET'])
@schema.route('/sources/', methods=['GET'])
@cross_origin(origins='*')
def list_sources_service():
    try:
        out = list_sources()
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@schema.route('/sources/<source_name>', methods=['GET'])
@schema.route('/sources/<source_name>/', methods=['GET'])
@cross_origin(origins='*')
def list_services(source_name):
    try:
        config = read_config_file_json(source_name, 'data_providers')
        out = {
            'base_url': config['services_base_url'],
            'services': config['services']
        }
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except Exception, err:
        raise PGeoException(errors[511], status_code=511)