# -*- coding: utf-8 -*-
import dj_database_url
import os
import urlparse


def combine_settings(settings_module, _locals):
    _locals.update(getattr(settings_module, 'REPLACE', {}))
    for k, v in getattr(settings_module, 'MERGE', {}).items():
        if isinstance(v, dict):
            _locals[k].update(v)
        else:
            _locals[k] += _locals[k].__class__(v)


def setup_database(varname, default):
    # TODO: (JFrancese) contribute back to dj_database_url
    if 'mssql' not in urlparse.uses_netloc:
        urlparse.uses_netloc.append('mssql')
    dj_database_url.SCHEMES['mssql'] = 'sqlserver_ado'
    url = str_from_env(varname, default)
    if not url:
        return None
    config = dj_database_url.parse(url)
    config['OPTIONS'] = {}
    if url[0:5] == 'mssql':
        config['OPTIONS']['use_legacy_date_fields'] = False
    query = urlparse.parse_qs(urlparse.urlparse(url).query)
    for k, v in query.items():
        if k.strip().lower() == 'conn_max_age':
            if v.strip().lower() == 'none':
                config['CONN_MAX_AGE'] = None
            else:
                config['CONN_MAX_AGE'] = int(v.strip())
            continue
        if v.strip().lower() == 'false':
            v = False
        elif v.strip().lower() == 'true':
            v = True
        elif v.strip().lower() == 'none':
            v = None
        config['OPTIONS'][k] = v
    return config


def str_from_env(varname, default=None):
    val = os.environ.get(varname, None)
    if val is None or val.strip() == '':
        return default
    elif val.strip().lower() == 'none':
        return None
    else:
        return val.decode('utf-8')


def bool_from_env(varname, default=None):
    val = os.environ.get(varname, '').strip().lower()
    if val == '':
        return default
    elif val == 'none':
        return None
    elif val in ('0', 'false', 'f', 'n', 'no', 'off'):
        return False
    else:
        return True


def int_from_env(varname, default=None):
    val = os.environ.get(varname, '').strip().lower()
    if val == '':
        return default
    elif val == 'none':
        return None
    else:
        return int(val)


def eval_from_env(varname, default=None):
    val = os.environ.get(varname, None)
    if val is None or val.strip() == '':
        return default
    else:
        return eval(val.decode('utf-8'))
