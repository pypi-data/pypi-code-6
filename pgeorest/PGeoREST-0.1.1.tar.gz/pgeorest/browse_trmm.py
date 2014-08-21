from ftplib import FTP
import json
from flask import Blueprint
from flask import Response
from flask.ext.cors import cross_origin
from pgeo.config.settings import read_config_file_json
from pgeo.error.custom_exceptions import PGeoException
from pgeo.error.custom_exceptions import errors
from pgeo.dataproviders import trmm as t


browse_trmm = Blueprint('browse_trmm', __name__)
conf = read_config_file_json('trmm', 'data_providers')


@browse_trmm.route('/')
@cross_origin(origins='*')
def list_years_service():
    try:
        out = t.list_years()
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@browse_trmm.route('/<year>')
@browse_trmm.route('/<year>/')
@cross_origin(origins='*')
def list_months_service(year):
    try:
        out = t.list_months(year)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())


@browse_trmm.route('/<year>/<month>')
@browse_trmm.route('/<year>/<month>/')
@cross_origin(origins='*')
def list_layers_service(year, month):
    try:
        out = t.list_layers(year, month)
        return Response(json.dumps(out), content_type='application/json; charset=utf-8')
    except PGeoException, e:
        raise PGeoException(e.get_message(), e.get_status_code())