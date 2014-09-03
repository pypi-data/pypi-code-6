import json
from flask import Blueprint
from flask import Response
from flask.ext.cors import cross_origin
from pgeo.config.settings import read_config_file_json
from pgeo.error.custom_exceptions import PGeoException
from pgeo.dataproviders import trmm2 as t


browse_trmm2 = Blueprint('browse_trmm2', __name__)
conf = read_config_file_json('trmm2', 'data_providers')


@browse_trmm2.route('/')
@cross_origin(origins='*')
def list_years_service():
    try:
        out = t.list_years()
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@browse_trmm2.route('/<year>')
@browse_trmm2.route('/<year>/')
@cross_origin(origins='*')
def list_months_service(year):
    try:
        out = t.list_months(year)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@browse_trmm2.route('/<year>/<month>')
@browse_trmm2.route('/<year>/<month>/')
@cross_origin(origins='*')
def list_days_service(year, month):
    try:
        out = t.list_days(year, month)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@browse_trmm2.route('/<year>/<month>/<day>')
@browse_trmm2.route('/<year>/<month>/<day>/')
@cross_origin(origins='*')
def list_layers_service(year, month, day):
    try:
        out = t.list_layers(year, month, day)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@browse_trmm2.route('/<year>/<month>/<from_day>/<to_day>')
@browse_trmm2.route('/<year>/<month>/<from_day>/<to_day>/')
@cross_origin(origins='*')
def list_layers_subset_service(year, month, from_day, to_day):
    try:
        out = t.list_layers_subset(year, month, from_day, to_day)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())