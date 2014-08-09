# -*- coding: utf-8 -*-
"""
AUTOREST_SOURCES:
    {
        'test': {
            'uri': 'mysql://root:@localhost/test_stat',
            'engine_kwargs': {
                'pool_size': 1,
                'pool_recycle': -1,
                'max_overflow': 0,
            },
            'auth': ('admin', 'admin'),
            'tables': {
                    'user': {
                        'per_page': 10,
                        'max_per_page': 100,
                    }
                },
            }
        }
    }
AUTOREST_BLUEPRINT_NAME
AUTOREST_URL_PREFIX

"""

__version__ = '0.1.1'

from math import ceil
import datetime
from flask.views import MethodView
from flask import Blueprint, jsonify, abort, request, Response
import dataset
from threading import Lock

DEFAULT_BLUEPRINT_NAME = 'autorest'
DEFAULT_URL_PREFIX = '/autorest'

DEFAULT_PER_PAGE = 1000
# -1 代表不限制
DEFAULT_MAX_PER_PAGE = -1


def autorest_jsonify(**kwargs):

    result_dict = dict()

    for k, v in kwargs.items():
        if isinstance(v, (datetime.datetime, datetime.date)):
            v = v.isoformat()

        result_dict[k] = v

    return jsonify(**result_dict)


class AutoRest(object):

    databases = None
    db_alloc_lock = None

    def __init__(self, app=None):
        """init with app

        :app: Flask instance

        """
        self.databases = dict()
        self.db_alloc_lock = Lock()

        if app:
            self.init_app(app)

    def init_app(self, app):
        """
        生成一个blueprint，安装到app上
        """

        blueprint_name = app.config.get('AUTOREST_BLUEPRINT_NAME') or DEFAULT_BLUEPRINT_NAME
        url_prefix = app.config.get('AUTOREST_URL_PREFIX') or DEFAULT_URL_PREFIX
        sources = app.config.get('AUTOREST_SOURCES')

        bp = Blueprint(blueprint_name, __name__, url_prefix=url_prefix)

        for db_name, db_conf in sources.items():
            bp.add_url_rule('/%s/<tb_name>/<pk>' % db_name,
                            view_func=ResourceView.as_view(
                                '%s' % db_name,
                                autorest=self,
                                db_name=db_name,
                                db_conf=db_conf,
                            )
            )

            bp.add_url_rule('/%s/<tb_name>' % db_name,
                            view_func=ResourceListView.as_view(
                                '%s_list' % db_name,
                                autorest=self,
                                db_name=db_name,
                                db_conf=db_conf,
                            )
            )

        app.register_blueprint(bp)


class AutoRestMethodView(MethodView):

    def __init__(self, autorest, db_name, db_conf):
        super(AutoRestMethodView, self).__init__()
        self.autorest = autorest
        self.db_name = db_name
        self.db_conf = db_conf

    def get_tb(self, tb_name):
        if tb_name not in self.db_conf['tables']:
            # 说明不存在
            return None, None

        uri = self.db_conf['uri']
        db = self.autorest.databases.get(self.db_name)
        if not db:
            try:
                self.autorest.db_alloc_lock.acquire()
                db = self.autorest.databases.get(self.db_name)
                if not db:
                    db = self.autorest.databases[self.db_name] = dataset.connect(
                        uri,
                        engine_kwargs=self.db_conf.get('engine_kwargs')
                    )
            finally:
                self.autorest.db_alloc_lock.release()

        tb = db[tb_name]
        pk_name = tb.table.primary_key.columns.values()[0].name
        return tb, pk_name

    def dispatch_request(self, *args, **kwargs):
        auth_conf = self.db_conf.get('auth')
        if auth_conf:
            if not request.authorization or \
                            (request.authorization.username, request.authorization.password) != tuple(auth_conf):
                # 权限验证失败
                abort(403)
                return

        return super(AutoRestMethodView, self).dispatch_request(*args, **kwargs)


class ResourceView(AutoRestMethodView):
    """
    /resource/<id>
    """
    def get(self, tb_name, pk):
        tb, pk_name = self.get_tb(tb_name)
        if tb is None or pk_name is None:
            abort(403)
            return

        kwargs = {
            pk_name: pk
        }

        obj = tb.find_one(**kwargs)
        if not obj:
            abort(404)
            return
        return autorest_jsonify(
            **obj
        )

    def patch(self, tb_name, pk):
        json_data = request.get_json(force=True)

        tb, pk_name = self.get_tb(tb_name)
        if tb is None or pk_name is None:
            abort(403)
            return

        json_data.update({
            pk_name: pk
        })

        tb.update(json_data, [pk_name])

        kwargs = {
            pk_name: pk
        }

        obj = tb.find_one(**kwargs)
        if not obj:
            abort(404)
            return
        return autorest_jsonify(
            **obj
        )

    put = patch

    def delete(self, tb_name, pk):
        tb, pk_name = self.get_tb(tb_name)
        if tb is None or pk_name is None:
            abort(403)
            return

        kwargs = {
            pk_name: pk
        }

        tb.delete(**kwargs)

        return Response(status=204)


class ResourceListView(AutoRestMethodView):
    """
    /resource/
    """

    def options(self, tb_name):
        tb, pk_name = self.get_tb(tb_name)
        if tb is None or pk_name is None:
            abort(403)
            return

        return autorest_jsonify(
            columns=tb.columns
        )

    def get(self, tb_name):
        tb, pk_name = self.get_tb(tb_name)
        if tb is None or pk_name is None:
            abort(403)
            return

        conf_per_page = self.db_conf['tables'][tb_name].get('per_page') or DEFAULT_PER_PAGE
        conf_max_per_page = self.db_conf['tables'][tb_name].get('max_per_page', DEFAULT_MAX_PER_PAGE)

        page = request.args.get('page', type=int) or 1
        per_page = request.args.get('per_page', type=int)

        if not per_page:
            per_page = conf_per_page

        if per_page > conf_max_per_page > 0:
            per_page = conf_max_per_page

        total = len(tb)
        pages = int(ceil(total / float(per_page)))

        obj_list = tb.find(_limit=per_page, _offset=(page-1)*per_page)
        json_obj_list = [obj for obj in obj_list]

        return autorest_jsonify(
            total=total,
            pages=pages,
            page=page,
            per_page=per_page,
            objects=json_obj_list
        )

    def post(self, tb_name):
        json_data = request.get_json(force=True)

        tb, pk_name = self.get_tb(tb_name)
        if tb is None or pk_name is None:
            abort(403)
            return

        pk = tb.insert(json_data)

        kwargs = {
            pk_name: pk
        }

        obj = tb.find_one(**kwargs)
        if not obj:
            abort(404)
            return
        return autorest_jsonify(
            **obj
        )
