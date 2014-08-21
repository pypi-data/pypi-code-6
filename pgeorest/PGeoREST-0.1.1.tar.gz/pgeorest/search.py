from flask import Blueprint
from flask import Response
from flask.ext.cors import cross_origin
from pgeo.metadata.search import MongoSearch
from bson import json_util
from pgeo.config.settings import settings


search = Blueprint('search', __name__)
connection = settings['db']['metadata']['connection']
db = settings['db']['metadata']['database']
doc = settings['db']['metadata']['document']['layer']
mongo_search = MongoSearch(connection, db, doc)


@search.route('/')
@cross_origin(origins='*')
def index():
    return 'Welcome to the Schema module!'


@search.route('/layer/id/<id>', methods=['GET'])
@search.route('/layer/id/<id>/', methods=['GET'])
@cross_origin(origins='*')
def find_layer_by_id_service(id):
    out = json_util.dumps(mongo_search.find_layer_by_id(id))
    return Response(out, content_type='application/json; charset=utf-8')


@search.route('/layer/dekad/<dekad>', methods=['GET'])
@search.route('/layer/dekad/<dekad>/', methods=['GET'])
@cross_origin(origins='*')
def find_layer_by_dekad_service(dekad):
    out = json_util.dumps(mongo_search.find_layers_by_product(None, dekad, None))
    return Response(out, content_type='application/json; charset=utf-8')


@search.route('/layer/product/<product>', methods=['GET'])
@search.route('/layer/product/<product>/', methods=['GET'])
@cross_origin(origins='*')
def find_layer_by_product_service(product):
    out = json_util.dumps(mongo_search.find_layers_by_product(product, None, None))
    return Response(out, content_type='application/json; charset=utf-8')


@search.route('/layer/product/<product>/dekad/<dekad>', methods=['GET'])
@search.route('/layer/product/<product>/dekad/<dekad>/', methods=['GET'])
@cross_origin(origins='*')
def find_layer_by_product_and_dekad_service(product, dekad):
    out = json_util.dumps(mongo_search.find_layers_by_product(product, dekad, None))
    return Response(out, content_type='application/json; charset=utf-8')


@search.route('/layer/product/<product>/dekad/<dekad>/type/<aggregation_type>', methods=['GET'])
@search.route('/layer/product/<product>/dekad/<dekad>/type/<aggregation_type>/', methods=['GET'])
@cross_origin(origins='*')
def find_layer_by_product_and_dekad_and_type_service(product, dekad, aggregation_type):
    out = json_util.dumps(mongo_search.find_layers_by_product(product, dekad, aggregation_type))
    return Response(out, content_type='application/json; charset=utf-8')


@search.route('/layer/from/<dekad_from>/to/<dekad_to>/product/<product>', methods=['GET'])
@search.route('/layer/from/<dekad_from>/to/<dekad_to>/product/<product>/', methods=['GET'])
@cross_origin(origins='*')
def find_layer_by_dekad_range(dekad_from, dekad_to, product):
    out = json_util.dumps(mongo_search.find_layers_by_dekad_range(dekad_from, dekad_to, product))
    return Response(out, content_type='application/json; charset=utf-8')


@search.route('/layer/from/<dekad_from>/to/<dekad_to>', methods=['GET'])
@search.route('/layer/from/<dekad_from>/to/<dekad_to>/', methods=['GET'])
@cross_origin(origins='*')
def find_layer_by_dekad_range_and_product(dekad_from, dekad_to):
    out = json_util.dumps(mongo_search.find_layers_by_dekad_range(dekad_from, dekad_to, None))
    return Response(out, content_type='application/json; charset=utf-8')