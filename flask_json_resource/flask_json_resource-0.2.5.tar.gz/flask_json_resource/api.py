import os
import hashlib
import json

from flask import Blueprint, current_app

import json_resource

from . import resources
from . import views


class FlaskResourceMixin(object):
    @property
    def etag(self):
        return hashlib.md5(json.dumps(self)).hexdigest()

    @classmethod
    def collection(self):
        db = current_app.extensions['json_resource'].db

        return db[self.schema['id']]


class API(object):

    def __init__(self, import_name, app=None, db=None, *args, **kwargs):
        self.blueprint = Blueprint('json_resource', import_name)

        resources.Schema.register_schema_dir(
            os.path.join(self.blueprint.root_path, 'schemas')
        )

        self.register()(resources.Schema)

        class Resource(FlaskResourceMixin, json_resource.Resource):
            default_views = (
                views.ResourceView, views.ResourceCreateView
            )

        class Collection(FlaskResourceMixin, json_resource.Collection):
            default_views = (views.CollectionView, )

        self.Resource = Resource
        self.Collection = Collection

        if app:
            self.init_app(app, db)

    def init_app(self, app, mongo):
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['json_resource'] = self

        app.register_blueprint(self.blueprint)

        self.mongo = mongo

    @property
    def db(self):
        return self.mongo.db

    def register(self, views=None, authorization=None):
        def _register(resource_cls):
            _views = views or resource_cls.default_views

            for view in _views:
                if authorization:
                    view = view(resource_cls, authorization())
                else:
                    view = view(resource_cls)

                if view.route:
                    self.blueprint.route(view.route, **view.options)(view)

            return resource_cls

        return _register
