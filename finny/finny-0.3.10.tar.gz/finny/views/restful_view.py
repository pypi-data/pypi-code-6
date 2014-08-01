import sys

import json
from collections import OrderedDict
from functools import wraps

import inflect
from flask import Response, request

from sqlalchemy import and_
from sqlalchemy.orm import class_mapper
from sqlalchemy.ext.declarative import DeclarativeMeta

from finny.exceptions import HttpNotFound

from flask import current_app
from flask import request

#
#

class AlchemyEncoder(json.JSONEncoder):

  def _encode_declarative_meta(self, obj):
    # an SQLAlchemy class
    fields = {}
    for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
      data = obj.__getattribute__(field)

      if field in [ "query", "query_class" ]:
        continue

      try:
        json.dumps(data) # this will fail on non-encodable values, like other classes
        fields[field] = data
      except TypeError:
        fields[field] = None
    # a json-encodable dict
    return fields

  def default(self, obj):
    if isinstance(obj.__class__, DeclarativeMeta):
      return self._encode_declarative_meta(obj)

    return json.JSONEncoder.default(self, obj)

def serialize(func):
  @wraps(func)
  def endpoint_method(*args, **kwargs):
    response = func(*args, **kwargs)

    if isinstance(response, Response):
      return response

    return Response(json.dumps(response, cls=AlchemyEncoder),  mimetype='application/json')

  return endpoint_method

class KaBoomError(Exception):
  status_code = 500

  def __init__(self, message, status_code=None, payload=None):
    Exception.__init__(self)
    self.message = message
    if status_code is not None:
      self.status_code = status_code
    self.payload = payload

  def to_dict(self):
    rv = dict(self.payload or ())
    rv['message'] = self.message
    return rv

def catch_it_all(func):
  @wraps(func)
  def endpoint_method(*args, **kwargs):
    if "DISABLED_ERROR_HANDLING" not in current_app.config:
      try:
        response = func(*args, **kwargs)
      except:
        current_app.config["SSENTRY"].captureException()
        raise KaBoomError("An error occured")
    else:
      response = func(*args, **kwargs)

    return response

  return endpoint_method

import inspect
from functools import partial

class ResourceBuilder(object):

  DAG = {}

  @classmethod
  def register(cls, klass):
    parent_klass = None
    if hasattr(klass, "__parent__"):
      parent_klass = klass.__parent__

    cls.DAG[klass] = parent_klass

  def __init__(self):
    pass

  def _get_parent_klasses(self, klass):
    def _get_parent(klass):
      if self.DAG[klass] == None:
        return []
      else:
        parent = self.DAG[klass]
        return [ parent ] + _get_parent(parent)

    return _get_parent(klass)

  def _resource_name(self, klass):

    if hasattr(klass, "route_base"):
      resource_name = klass.route_base
    else:
      resource_name = klass.__name__.lower()
      pos = resource_name.find("view")

      if pos == -1:
        raise AttributeError("Resource %s doesn't end in View" % resource_name)

      resource_name = resource_name[:pos]

    return resource_name

  def _make_show_url(self, klass):
    resource_name = self._resource_name(klass)
    """
    Resource Name can either be a single name OR _ separted words.
    If it's just a word for the param ID make it singular, for the
    underscore separated words make the last part singular
    """

    engine = inflect.engine()

    split_name = resource_name.split("_")
    entity_id  = engine.singular_noun(split_name[-1])

    if not entity_id:
      entity_id = split_name[-1]

    # ID must be singular
    return "/%s/<%s_id>" % (resource_name, entity_id)

  def _add_route(self, klass, url, method_name, http_verbs):
    methods = dict(inspect.getmembers(klass, predicate=inspect.ismethod))

    def call_method(method_name):
      instance = klass()

      method = getattr(instance, method_name)

      if hasattr(klass, "decorators"):
        for d in klass.decorators:
          method = d(method)

      return method

    if hasattr(klass, method_name) and method_name in methods:
      self.app.add_url_rule(url,
                            "%s::%s" % (klass.__name__, method_name),
                            call_method(method_name),
                            methods=http_verbs)
      # TODO: Why this?
      setattr(klass, "_orig_%s" % method_name, getattr(klass, method_name))
      setattr(klass, method_name, call_method(method_name))

  def _add_bypass_route(self, klass, url):
    # get all the available methods
    methods = dict(inspect.getmembers(klass, predicate=inspect.ismethod))

    def update_delete_bypass(ctx, **kwargs):
      http_verb = request.args.get('method')

      if http_verb == "put":
        return ctx._orig_update(**kwargs)
      elif http_verb == "delete":
        return ctx._orig_delete(**kwargs)
      else:
        raise AttributeError("Method is neither update or delete")

    # explicit put method in class
    setattr(klass, "update_delete_bypass", update_delete_bypass)

    def call_method(method_name):
      instance = klass()

      method = getattr(instance, method_name)

      if hasattr(klass, "decorators"):
        for d in klass.decorators:
          method = d(method)

      return method

    method_name = "update_delete_bypass"

    self.app.add_url_rule(url,
                          "%s::%s" % (klass.__name__, method_name),
                          call_method(method_name),
                          methods=["POST"])

    setattr(klass, "_orig_%s" % method_name, getattr(klass, method_name))
    setattr(klass, method_name, call_method(method_name))


  def _add_nested_route(self, app, klass, parent_klasses):
    """
    resource_name

    make_show_url(klass, name)
    """

    base_url = [ self._make_show_url(parent) for parent in reversed(parent_klasses) ]
    base_url = "".join(base_url)

    resource_name = self._resource_name(klass)
    resource_base = "%s/%s" % (base_url, resource_name)

    self._add_restful_routes(app, klass, resource_name, resource_base)

  def _add_restful_routes(self, app, klass, resource_name, resource_base):
    self.app = app

    engine = inflect.engine()
    split_name = resource_name.split("_")

    entity_id = engine.singular_noun(split_name[-1])
    if not entity_id:
      entity_id = split_name[-1]

    if "index" not in klass.except_methods:
      self._add_route(klass, resource_base, "index", ["GET"])

    if "create" not in klass.except_methods:
      self._add_route(klass, resource_base, "create", ["POST"])

    if "show" not in klass.except_methods:
      self._add_route(klass, resource_base + "/<%s_id>" % entity_id, "show", ["GET"])

    if "update" not in klass.except_methods:
      self._add_route(klass, resource_base + "/<%s_id>" % entity_id, "update", ["PUT"])

    if "delete" not in klass.except_methods:
      self._add_route(klass, resource_base + "/<%s_id>" % entity_id, "delete", ["DELETE"])

    self._add_bypass_route(klass, resource_base + "/<%s_id>" % entity_id)

  def _add_normal_route(self, app, klass):
    methods = dict(inspect.getmembers(klass, predicate=inspect.ismethod))

    resource_name = self._resource_name(klass)
    resource_base = "/" + resource_name

    self._add_restful_routes(app, klass, resource_name, resource_base)

  def build(self, app):
    for klass, klass_parent in self.DAG.iteritems():
      if klass_parent:
        parent_klasses = self._get_parent_klasses(klass)
        self._add_nested_route(app, klass, parent_klasses)
      else:
        self._add_normal_route(app, klass)

class Resource(object):

  decorators = [ serialize, catch_it_all ]

  @classmethod
  def register(cls):
    ResourceBuilder.register(cls)

class ModelResource(Resource):

  """
  Is nested than build the resources first
  """

  decorators = [ serialize, catch_it_all ]

  def index(self, **kwargs):
    if self.__is_nested():
      parents = self.__get_parents()
      models = self.__get_models(parents)
      model_ids = self.__get_model_ids(models)
      args_to_model = self.__get_args(parents, kwargs)

      query = self.db.session.query(self.model)

      for model in models.keys():
        query = query.join(getattr(model, models[model]))

      and_params = []
      for model in models.keys():
        pk_for_model = getattr(model, model_ids[model])
        key_name = args_to_model[model]
        and_params.append(pk_for_model.__eq__(kwargs[key_name]))

      items = query.filter(and_(*and_params)).all()
    else:
      items = self.model.query.all()

    return items

  def __get_args(self, parents, kwargs):
    engine = inflect.engine()

    args = {}

    for p in parents:
      name = p.__name__.lower()
      pos = name.find("view")
      arg = name[:pos]

      arg = arg.split("_")
      entity_id = engine.singular_noun(arg[-1])

      if not entity_id:
        entity_id = arg[-1]

      if ("%s_id" % entity_id) in kwargs:
        args[p.model] = "%s_id" % entity_id

    return args

  def __get_model_ids(self, models):
    return dict([ [m , class_mapper(m).primary_key[0].name] for m in models.keys() ])

  def __get_models(self, parents):
    models = dict([ [p, p.model] for p in parents ])

    to_assoc = OrderedDict()

    for p in range(len(parents)):
      if p == len(parents) - 1:
        continue

      parent = parents[p]
      associated = parents[p+1]
      assoc_name = models[associated].__tablename__

      if (assoc_name in models[parent].__backref__ and
          hasattr(models[parent], assoc_name)):
        to_assoc[models[parent]] = assoc_name
      else:
        raise LookupError("When calling a nested route you need to have a relationship backref from %s to %s named %s" % (model[parent], model[associated], assoc_name))

    return to_assoc

  def create(self, **kwargs):
    data = json.loads(request.data)
    item = self.model(**data)

    """
    You need the parent of the object that you will create
    """
    if self.__is_nested():
      parents = self.__get_parents()
      models = self.__get_models(parents)
      model_ids = self.__get_model_ids(models)
      args_to_model = self.__get_args(parents, kwargs)

      parent_view = parents[-2]
      parent_model = parent_view.model
      query = self.db.session.query(parent_model)

      join_models = models.keys()
      join_models.remove(parent_model)

      for model in join_models:
        query = query.join(getattr(model, models[model]))

      and_params = []
      for model in models.keys():
        pk_for_model = getattr(model, model_ids[model])
        key_name = args_to_model[model]
        and_params.append(pk_for_model.__eq__(kwargs[key_name]))

      parent_item = query.filter(and_(*and_params)).first()
      assoc_key = models[parent_model]
      assoc_list = getattr(parent_item, assoc_key)
      assoc_list.append(item)

    self.db.session.add(item)
    self.db.session.commit()

    return item

  def show(self, **kwargs):
    if self.__is_nested():
      parents = self.__get_parents()
      models = self.__get_models(parents)
      model_ids = self.__get_model_ids(models)
      args_to_model = self.__get_args(parents, kwargs)

      query = self.db.session.query(self.model)

      current_model_id = class_mapper(self.model).primary_key[0].name
      model_ids[self.model] = current_model_id

      for model in models.keys():
        query = query.join(getattr(model, models[model]))

      and_params = []
      for model in models.keys() + [ self.model ]:
        pk_for_model = getattr(model, model_ids[model])
        key_name = args_to_model[model]
        and_params.append(pk_for_model.__eq__(kwargs[key_name]))

      item = query.filter(and_(*and_params)).first()
    else:
      key = kwargs.keys()[0]
      item = self.model.query.get(kwargs[key])

    if not item:
      raise HttpNotFound({'error': 'Item not found in database'})

    return item

  def update(self, **kwargs):
    # TODO: Refactor this as the logic is the same for the show and update methods
    data = json.loads(request.data)
    if self.__is_nested():
      parents = self.__get_parents()
      models = self.__get_models(parents)
      model_ids = self.__get_model_ids(models)
      args_to_model = self.__get_args(parents, kwargs)

      query = self.db.session.query(self.model)

      current_model_id = class_mapper(self.model).primary_key[0].name
      model_ids[self.model] = current_model_id

      for model in models.keys():
        query = query.join(getattr(model, models[model]))

      and_params = []
      for model in models.keys() + [ self.model ]:
        pk_for_model = getattr(model, model_ids[model])
        key_name = args_to_model[model]
        and_params.append(pk_for_model.__eq__(kwargs[key_name]))

      item = query.filter(and_(*and_params)).first()
    else:
      key = kwargs.keys()[0]
      item = self.model.query.get(kwargs[key])

    if not item:
      raise HttpNotFound({'error': 'Item not found in database'})

    for field in data:
      if hasattr(item, field):
        setattr(item, field, data[field])

    self.db.session.add(item)
    self.db.session.commit()

    return item

  def delete(self, **kwargs):
    # TODO: Refactor this as the logic is the same for the show and update methods
    if self.__is_nested():
      parents = self.__get_parents()
      models = self.__get_models(parents)
      model_ids = self.__get_model_ids(models)
      args_to_model = self.__get_args(parents, kwargs)

      query = self.db.session.query(self.model)

      current_model_id = class_mapper(self.model).primary_key[0].name
      model_ids[self.model] = current_model_id

      for model in models.keys():
        query = query.join(getattr(model, models[model]))

      and_params = []
      for model in models.keys() + [ self.model ]:
        pk_for_model = getattr(model, model_ids[model])
        key_name = args_to_model[model]
        and_params.append(pk_for_model.__eq__(kwargs[key_name]))

      item = query.filter(and_(*and_params)).first()
    else:
      key = kwargs.keys()[0]
      item = self.model.query.get(kwargs[key])

    if not item:
      raise HttpNotFound({'error': 'Item not found in database'})

    self.db.session.delete(item)
    self.db.session.commit()

    return {'success': 'Item was deleted!'}

  def __is_nested(self):
    return hasattr(self, "__parent__")

  def __get_parents(self, **kwargs):
    """
    From base to root
    """
    def _get_parent(klass):
      if not hasattr(klass, "__parent__"):
        return []
      else:
        parent = klass.__parent__
        return [ parent ] + _get_parent(parent)

    return _get_parent(self)[::-1] + [ self.__class__ ]
