import json
from flask import Blueprint
from flask import Response
from flask.ext.cors import cross_origin
from pgeo.error.custom_exceptions import PGeoException
from pgeotrmm.core import trmm_core as t


trmm = Blueprint('trmm', __name__)


@trmm.route('/')
@cross_origin(origins='*')
def list_years_service():
    try:
        out = t.list_years()
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@trmm.route('/<year>')
@trmm.route('/<year>/')
@cross_origin(origins='*')
def list_months_service(year):
    try:
        out = t.list_months(year)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@trmm.route('/<year>/<month>')
@trmm.route('/<year>/<month>/')
@cross_origin(origins='*')
def list_days_service(year, month):
    try:
        out = t.list_days(year, month)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@trmm.route('/<year>/<month>/<day>')
@trmm.route('/<year>/<month>/<day>/')
@cross_origin(origins='*')
def list_layers_service(year, month, day):
    try:
        out = t.list_layers(year, month, day)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@trmm.route('/<year>/<month>/<from_day>/<to_day>')
@trmm.route('/<year>/<month>/<from_day>/<to_day>/')
@cross_origin(origins='*')
def list_layers_subset_service(year, month, from_day, to_day):
    try:
        out = t.list_layers_subset(year, month, from_day, to_day)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@trmm.route('/layers/<year>/<month>')
@trmm.route('/layers/<year>/<month>/')
@cross_origin(origins='*')
def list_layers_month_subset_service(year, month):
    try:
        out = t.list_layers_month_subset(year, month)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())