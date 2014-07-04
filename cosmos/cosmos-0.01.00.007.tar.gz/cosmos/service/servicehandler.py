from cosmos.service import requesthandler

__author__ = 'Maruf Maniruzzaman'

import tornado.ioloop
import tornado.web
import tornado.options
import tornado.template
import tornado.websocket
from tornado import gen

from cosmos.service.utils import MongoObjectJSONEncoder
from cosmos.dataservice.objectservice import *

class ServiceHandler(requesthandler.RequestHandler):
    @tornado.web.asynchronous
    def get(self, object_path):
        params = object_path.split('/')
        object_name = params[0]
        id = params[1]

        db = self.settings['db']

        obj_serv = ObjectService()
        columns_str = self.get_argument("columns", None)
        filter_str = self.get_argument("filter", None)

        if filter_str:
            query=json.loads(filter_str)
        else:
            query=None

        if columns_str:
            columns = columns_str.split(',')
            columns = [column.strip() for column in columns]
        else:
            columns = []

        if id and len(id)>0:
            obj_serv.load(self.current_user, db, object_name, id, columns, self._on_load_response)
        else:
            obj_serv.find(self.current_user, db, object_name, query, columns, self._on_load_response)

    def _on_load_response(self, result, error):
        logging.debug("ServiceHandler::_on_response. Error = {0} ".format(error))
        if error:
            raise tornado.web.HTTPError(500, error)
        else:
            self.content_type = 'application/json'
            data = MongoObjectJSONEncoder().encode(result)
            self.write(data)
            self.finish()

    def _on_response(self, result, error):
        logging.debug("ServiceHandler::_on_response. Error = {0} ".format(error))
        if error:
            raise tornado.web.HTTPError(500, error)
        else:
            self.content_type = 'application/json'
            data = '{"result":"OK"}'
            self.write(data)
            self.finish()

    @tornado.web.asynchronous
    def post(self, object_path):
        params = object_path.split('/')
        object_name = params[0]

        data = json.loads(self.request.body)
        assert isinstance(data, dict)

        db = self.settings['db']

        obj_serv = ObjectService()
        obj_serv.save(self.current_user, db, object_name,data, self._on_response)


    @tornado.web.asynchronous
    def put(self, object_path):
        params = object_path.split('/')
        object_name = params[0]
        id = params[1]

        data = json.loads(self.request.body)
        assert isinstance(data, dict)

        db = self.settings['db']
        obj_serv = ObjectService()
        obj_serv.update(self.current_user, db, object_name, id, data, self._on_response)


    @tornado.web.asynchronous
    def delete(self, object_path):
        params = object_path.split('/')
        object_name = params[0]
        id = params[1]

        db = self.settings['db']
        obj_serv = ObjectService()
        obj_serv.delete(self.current_user, db, object_name, id, self._on_response)





