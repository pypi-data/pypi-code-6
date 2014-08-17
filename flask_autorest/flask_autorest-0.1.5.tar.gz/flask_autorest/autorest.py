# -*- coding: utf-8 -*-

from flask import Blueprint
from threading import Lock

from . import constants
from .views import ResourceView, ResourceListView


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

        blueprint_name = app.config.get('AUTOREST_BLUEPRINT_NAME') or constants.DEFAULT_BLUEPRINT_NAME
        url_prefix = app.config.get('AUTOREST_URL_PREFIX') or constants.DEFAULT_URL_PREFIX
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
