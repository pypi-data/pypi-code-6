import json
from flask import Blueprint
from flask import Response
from flask import request
from flask.ext.cors import cross_origin
from pgeo.error.custom_exceptions import PGeoException
from pgeomodis.core import modis_core as m


modis = Blueprint('modis', __name__)


@modis.route('/')
@cross_origin(origins='*')
def list_products_service():
    try:
        out = m.get_modis_product_table()
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@modis.route('/<product_name>')
@modis.route('/<product_name>/')
@cross_origin(origins='*')
def list_years_service(product_name):
    try:
        out = m.list_years(product_name)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@modis.route('/<product_name>/<year>')
@modis.route('/<product_name>/<year>/')
@cross_origin(origins='*')
def list_days_service(product_name, year):
    try:
        out = m.list_days(product_name, year)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@modis.route('/<product_name>/<year>/<day>')
@modis.route('/<product_name>/<year>/<day>/')
@cross_origin(origins='*')
def list_layers_service(product_name, year, day):
    try:
        out = m.list_layers(product_name, year, day)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@modis.route('/<product_name>/<year>/<day>/<from_h>/<to_h>/<from_v>/<to_v>')
@modis.route('/<product_name>/<year>/<day>/<from_h>/<to_h>/<from_v>/<to_v>/')
@cross_origin(origins='*')
def list_layers_subset_service(product_name, year, day, from_h, to_h, from_v, to_v):
    try:
        out = m.list_layers_subset(product_name, year, day, from_h, to_h, from_v, to_v)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@modis.route('/<product_name>/<year>/<day>/<countries>')
@modis.route('/<product_name>/<year>/<day>/<countries>/')
@cross_origin(origins='*')
def list_layers_countries_subset_service(product_name, year, day, countries):
    try:
        out = m.list_layers_countries_subset(product_name, year, day, countries)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@modis.route('/countries')
@modis.route('/countries/')
@cross_origin(origins='*')
def list_countries():
    print request.host_url

    try:
        out = m.list_countries()
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())