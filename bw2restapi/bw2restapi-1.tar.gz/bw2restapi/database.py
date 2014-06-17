from . import api_app
from bw2data import databases, JsonWrapper, Database
from flask import request, abort
from flask.views import MethodView
from bw2ui.web.utils import json_response


@api_app.route("/api/v1/databases/")
def list_databases():
    """Return a list of all available databases.

    URL is ``/api/v1/databases/``."""
    return json_response(sorted(databases.list))


@api_app.route("/api/v1/database/<database>/list/")
def list_activities_for_database(database):
    """Return a list of all activities for database ``database``.

    URL is ``/api/v1/database/<database>/list/``."""
    if database not in databases:
        abort(404)
    return json_response(sorted(Database(database).load().keys()))


class DatabaseAPI(MethodView):

    """
The base URL for activities is:

    */api/v1/database/<database name>/*

The following REST methods are available: GET, POST, DELETE.

    """

    def get(self, database):
        """
Get database metadata.

Response codes:

    * 200: Resource retrieved
    * 404: Resource not found

        """
        try:
            return JsonWrapper.dumps(databases[database])
        except KeyError:
            abort(404)

    def post(self, database):
        """
Create a new database.

Post data is optional, and should be a JSON hash table with values to be passed to the ``.register()`` method. To create a database with a JSON backend, send ``{"backend": "json"}``.

Response codes:

    * 201: Database created
    * 400: Can't decipher post data to valid JSON hash table
    * 409: Conflict - resource already exists

        """
        if database in databases:
            abort(409)  # Conflict: Resource already exists
        if request.data:
            try:
                kwargs = request.get_json(force=True)
                assert isinstance(kwargs, dict)
            except:
                abort(400)
        else:
            kwargs = {}
        Database(database, backend=kwargs.get('backend')).register(**kwargs)
        return 'OK', 201

    def delete(self, database):
        """
Delete an existing database.

Response codes:

    * 200: Resource delete succeeded
    * 404: Resource not found

        """
        try:
            del databases[database]
            return 'OK'
        except KeyError:
            abort(404)


api_app.add_url_rule('/api/v1/database/<database>/', view_func=DatabaseAPI.as_view('database'))
