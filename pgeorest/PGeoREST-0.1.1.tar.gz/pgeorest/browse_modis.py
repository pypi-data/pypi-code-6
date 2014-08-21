import json

from flask import Blueprint
from flask import Response
from flask.ext.cors import cross_origin

from pgeo.error.custom_exceptions import PGeoException

from pgeo.dataproviders import modis as m


browse_modis = Blueprint('browse_modis', __name__)


@browse_modis.route('/')
@cross_origin(origins='*')
def list_products_service():
    try:
        out = m.list_products()
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@browse_modis.route('/<product_name>')
@browse_modis.route('/<product_name>/')
@cross_origin(origins='*')
def list_years_service(product_name):
    try:
        out = m.list_years(product_name)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@browse_modis.route('/<product_name>/<year>')
@browse_modis.route('/<product_name>/<year>/')
@cross_origin(origins='*')
def list_days_service(product_name, year):
    try:
        out = m.list_days(product_name, year)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@browse_modis.route('/<product_name>/<year>/<day>')
@browse_modis.route('/<product_name>/<year>/<day>/')
@cross_origin(origins='*')
def list_layers_service(product_name, year, day):
    try:
        out = m.list_layers(product_name, year, day)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())