
from flask.ext.restful import reqparse
from flask.ext.restful import abort
from flask.ext.restful import Resource
from flask.ext.restful import fields
from flask.ext.restful import marshal_with

from sqlalchemy import inspect

PYTHON_RESTFUL_MAP = {
    'int': fields.Integer,
    'str': fields.String,
    'bool': fields.Boolean,
    'datetime': fields.DateTime,
    'float': fields.Float,
}


def make_fields(model):
    model_fields = {}
    mapper = inspect(model)
    for column in mapper.c:
        py_type = column.type.python_type.__name__
        model_fields[column.name] = PYTHON_RESTFUL_MAP[py_type]

    model_name = model.__tablename__[:-1]
    model_fields['uri'] = fields.Url(model_name, absolute=True)
    return model_fields

def make_parser(model):
    parser = reqparse.RequestParser()
    mapper = inspect(model)
    for column in mapper.c:
        parser.add_argument(column.name, type=column.type.python_type)
    return parser

def create_single_resource(model, session):
    model_fields = make_fields(model)
    parser = make_parser(model)

    class SingleResource(Resource):
        @marshal_with(model_fields)
        def get(self, id):
            model_instance = session.query(model).filter(model.id == id).first()
            if not model_instance:
                abort(404, message="model {} doesn't exist".format(id))
            return model_instance

        def delete(self, id):
            model_instance = session.query(model).filter(model.id == id).first()
            if not model_instance:
                abort(404, message="model {} doesn't exist".format(id))
            session.delete(model_instance)
            session.commit()
            return {}, 204

        @marshal_with(model_fields)
        def put(self, id):
            parsed_args = parser.parse_args()
            model_instance = session.query(model).filter(model.id == id).first()

            mapper = inspect(model)
            for column in mapper.c:
                setattr(model_instance, column.name, parsed_args[column.name])
            setattr(model_instance, 'id', id)

            session.merge(model_instance)
            session.commit()
            return model_instance, 201

    return SingleResource

def create_list_resource(model, session):
    model_fields = make_fields(model)
    parser = make_parser(model)

    class ListResource(Resource):
        @marshal_with(model_fields)
        def get(self):
            model_instances = session.query(model).all()
            return model_instances

        @marshal_with(model_fields)
        def post(self):
            parsed_args = parser.parse_args()
            model_instance = model()
            mapper = inspect(model)
            for column in mapper.c:
                setattr(model_instance, column.name, parsed_args[column.name])
            session.add(model_instance)
            session.commit()
            return model_instance, 201

    return ListResource
