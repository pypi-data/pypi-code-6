import collections
from mongolog import MongoHandler
import tornado
import logging
import pymongo
import cosmos
from cosmos.dataservice.objectservice import add_operation_preprocessor, ObjectService
from cosmos.rbac.object import *
from cosmos.rbac.service import update_role_cache


__author__ = 'Maruf Maniruzzaman (maruf@lekhoni.com)'


class BootLoader():
    def init_observers(self, observers):
        add_operation_preprocessor(cosmos.service.auth.before_user_insert, COSMOS_USERS_OBJECT_NAME, [AccessType.INSERT, AccessType.UPDATE])
        add_operation_preprocessor(cosmos.rbac.service.before_role_insert_update, cosmos.rbac.object.COSMOS_ROLE_OBJECT_NAME, [AccessType.INSERT, AccessType.UPDATE])

        for observer in observers:
            assert isinstance(observer, dict)
            func = observer["function"]
            object_name = observer["object_name"]
            access = observer["access"]
            assert isinstance(access, collections.Iterable)

            add_operation_preprocessor(func, object_name, access)


    def load_roles(self, db):
        object_service = ObjectService()
        object_name = COSMOS_ROLE_OBJECT_NAME
        columns = []
        object_service.find(SYSTEM_USER, db, object_name, None, columns, self._on_load_roles_response)

    def _on_load_roles_response(self, result, error):
        if error:
            raise tornado.web.HTTPError(500, error)
        else:
            for role in result:
                try:
                    update_role_cache(role)
                except ValueError, ve:
                    logging.exception("Role {0} could not be loaded.".format(role.get("name")))


    def config_mongolog(self, db_uri, db_name, log_col_name, log_level):
        c_sync = pymongo.MongoClient(db_uri, w=0)
        col = c_sync[db_name][log_col_name]
        logging.getLogger().addHandler(MongoHandler.to(collection=col))
        logging.getLogger().setLevel(log_level)