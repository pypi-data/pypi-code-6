import json
from flask import Blueprint
from flask import Response
from flask import request
from flask.ext.cors import cross_origin
from pgeo.error.custom_exceptions import PGeoException
from pgeo.error.custom_exceptions import errors
from pgeo.config.settings import settings
from pgeo.metadata.metadata import merge_layer_metadata
from pgeo.metadata.db_metadata import DBMetadata


metadata = Blueprint('metadata', __name__)


@metadata.route('/')
@cross_origin(origins='*')
def index():
    return 'Welcome to the Metadata module!'

DBMetadata = DBMetadata(settings["db"]["metadata"])


@metadata.route('/create', methods=['POST'])
@metadata.route('/create/', methods=['POST'])
@cross_origin(origins='*', headers=['Content-Type'])
def create():
    """
    Store a metadata in the MongoDB
    @return: Acknowledge in JSON format: status_code, status_message, mongo_id
    """
    try:
        user_json = request.get_json()
        merged = merge_layer_metadata('modis', user_json)
        mongo_id = str(DBMetadata.insert_metadata(merged))
        response = {'status_code': 200, 'status_message': 'OK', 'mongo_id': mongo_id}
        return Response(json.dumps(response), content_type='application/json; charset=utf-8')
    except:
        raise PGeoException(errors[513], status_code=513)


@metadata.route('/delete/<id>', methods=['DELETE'])
@metadata.route('/delete/<id>/', methods=['DELETE'])
@cross_origin(origins='*', headers=['Content-Type'])
def delete(id):
    """
    REST service to delete a metadata from the DB.
    @param id: ID of the resource to be deleted.
    @return: MongoDB message
    """
    try:
        out = DBMetadata.remove_metadata_by_id(id)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except:
        raise PGeoException(errors[513], status_code=513)