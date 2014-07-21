from . import api_app
from brightway2 import Database, databases
from bw2data.errors import UnknownObject
from bw2ui.web.utils import json_response
from copy import deepcopy
from flask import request, abort, url_for
from flask.views import MethodView


class ActivityAPI(MethodView):

    """
The base URL for activities is:

    */api/database/<database name>/activity/<activity key>/*

The following REST methods are available: GET, POST, PUT, DELETE.

    """

    def _tuplefy(self, data):
        """Make sure that exchange input keys are tuples"""
        for exchange in data.get('exchanges', []):
            if 'input' in exchange:
                exchange['input'] = tuple(exchange['input'])
        return data

    def _hydrate(self, data):
        """Add name, unit, location, url, and categories to exchanges"""
        if data.get("type", "process") != "process":
            return data
        for exc in data.get("exchanges", []):
            ds = Database(exc["input"][0]).load()[exc["input"]]
            for key in ("name", "url", "unit", "location", "categories"):
                exc[key] = deepcopy(ds.get(key))
            exc["url"] = url_for("activity", database=exc["input"][0], activity=exc["input"][1])
        return data

    def _dehydrate(self, data):
        """Remove name, unit, location, url, and categories from exchanges"""
        for exc in data.get("exchanges", []):
            for key in ("name", "unit", "location", "categories", "url"):
                if key in exc:
                    del exc[key]
        return data

    def get(self, database, activity):
        """
Get an activity dataset.

Response codes:

    * 200: Resource retrieved
    * 404: Resource not found

        """
        try:
            return json_response(self._hydrate(
                Database(database).load()[(database, activity)]
            ))
        except (KeyError, UnknownObject):
            abort(404)

    def post(self, database, activity):
        """
Create a new activity dataset.

Response codes:

    * 201: Activity dataset created
    * 400: No JSON body could be decoded
    * 404: Database not found
    * 409: Conflict - resource already exists

        """
        if database not in databases:
            abort(404)
        db_data = Database(database).load()
        if (database, activity) in db_data:
            abort(409)  # Conflict: Resource already exists
        db_data[(database, activity)] = self._tuplefy(
            request.get_json(force=True))
        return 'OK', 201

    def put(self, database, activity):
        """
Update an existing activity dataset.

Response codes:

    * 200: Resource update succeeded
    * 400: No JSON body could be decoded
    * 404: Resource not found

        """
        if database not in databases:
            abort(404)
        db_data = Database(database).load()
        if (database, activity) not in db_data:
            abort(404)  # Resource to update does not exist
        db_data[(database, activity)] = self._dehydrate(self._tuplefy(request.get_json(force=True)
        ))
        return 'OK'

    def delete(self, database, activity):
        """
Delete an existing activity dataset.

Response codes:

    * 200: Resource delete succeeded
    * 404: Resource not found

        """
        if database not in databases:
            abort(404)
        db_data = Database(database).load()
        if (database, activity) not in db_data:
            abort(404)
        else:
            del db_data[(database, activity)]
            return 'OK', 204


api_app.add_url_rule('/api/database/<database>/activity/<activity>/', view_func=ActivityAPI.as_view('activity'))
