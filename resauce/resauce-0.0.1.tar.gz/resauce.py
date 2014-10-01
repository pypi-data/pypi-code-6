from colanderalchemy import SQLAlchemySchemaNode
from flask import Response, request
from flask.views import View
import json
import colander
import dictalchemy.utils

class ResauceException(Exception):
    pass

class BadRequest(ResauceException):
    def __init__(self, error_dict):
        self.error_dict = error_dict

    def as_response(self):
        return Response(
            json.dumps(self.error_dict),
            status=400,
            mimetype="application/json"
        )

class NotFound(ResauceException):
    def as_response(self):
        response = {
            "message": "Not found!"
        }
        return Response(
            json.dumps(response),
            status=404,
            mimetype="application/json"
        )

class Resource(View):
    methods = ["GET", "PUT", "POST", "DELETE"]

    def do_get(self, id=None):
        if id is not None:
            result = self.get_resource(id)
            return self._render(result, many=False)
        result = self.get_collection()
        return self._render(result, many=True)

    def get_resource(self, id):
        result = self.get_session().query(self.model)\
            .filter_by(id=id)\
            .first()
        if result is None:
            raise NotFound()
        return result

    def get_schema(self):
        if hasattr(self, "schema"):
            return self.schema()
        return SQLAlchemySchemaNode(self.model, excludes=["id"])

    def serialize(self, data, many=False):
        if hasattr(self, "serializer"):
            return self.serializer(data, many=many).data
        if many:
            return [dictalchemy.utils.asdict(obj) for obj in data]
        else:
            return dictalchemy.utils.asdict(data)

    def get_collection(self):
        return self.get_session().query(self.model)

    def do_post(self):
        try:
            data = json.loads(request.data.decode("UTF-8"))
        except ValueError as ex:
            raise BadRequest({"message": "invalid json"})
        schema = self.get_schema()
        try:
            valid_data = schema.deserialize(data)
        except colander.Invalid as ex:
            raise BadRequest(ex.asdict())
        if hasattr(self, "post"):
            new_resource = self.post(valid_data)
        else:
            new_resource = self.model(**valid_data)
        session = self.get_session()
        session.add(new_resource)
        session.commit()
        return self._render(new_resource, status=201)

    def do_put(self, id):
        try:
            data = json.loads(request.data.decode("UTF-8"))
        except ValueError as ex:
            raise BadRequest({"message": "invalid json"})

        schema = self.get_schema()
        try:
            valid_data = schema.deserialize(data)
        except colander.Invalid as ex:
            raise BadRequest(ex.asdict())

        session = self.get_session()
        resource = session.query(self.model).filter_by(id=id).first()
        if resource is None:
            raise NotFound
        if hasattr(self, "put"):
            resource = self.put(resource, valid_data)
        else:
            dictalchemy.utils.fromdict(resource, data)
        session.add(resource)
        session.commit()
        return self._render(resource)

    def do_delete(self, id):
        session = self.get_session()
        resource = session.query(self.model).filter_by(id=id).first()
        if resource:
            session.delete(resource)
            session.commit()
            return Response(
                status=204,
                mimetype="application/json"
            )
        else:
            raise NotFound()

    def _render(self, data, many=False, status=200):
        return Response(
            json.dumps(self.serialize(data, many=many)),
            mimetype="application/json",
            status=status
        )

    def dispatch_request(self, *args, **kwargs):
        meth = getattr(self, "do_" + request.method.lower(), None)
        try:
            result = meth(*args, **kwargs)
        except ResauceException as ex:
            return ex.as_response()
        return result



def register_resource(resource, app, url):
    app.add_url_rule(
        url,
        view_func=resource.as_view(resource.name),
    )
    detail_name = resource.name + "-detail"
    app.add_url_rule(
        url + "/<id>",
        view_func=resource.as_view(detail_name)
    )

