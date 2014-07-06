import inspect
import datetime
import logging
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.template
import tornado.websocket
from bson import ObjectId

from cosmos.rbac.service import *


__author__ = 'Maruf Maniruzzaman'

#TODO: Use context class to implement postprocessor
class CallbackContext():
    def __init__(self, *args, **kwargs):
        pass

#TODO: Use observers to check access - initialize in the __init__ of the rbac package

ACCESS_TYPE_ROLE = 1
ACCESS_TYPE_OWNER_ONLY = 2

class ObjectService():
    def __init__(self, *args, **kwargs):
        self.rbac_service = RbacService()

    def check_access(self, user, object_name, properties, access, check_owner=False):
        roles = self.rbac_service.get_roles(user)
        for role in roles:
            has_access = self.rbac_service.has_access(role, object_name, properties, access)
            if has_access:
                return ACCESS_TYPE_ROLE

            if check_owner:
                has_owner_access = self.rbac_service.has_owner_access(role, object_name, properties, access)
                if has_owner_access:
                    return ACCESS_TYPE_OWNER_ONLY

        raise tornado.web.HTTPError(401, "Unauthorized")

    def save(self, user, db, object_name, data, callback):
        logging.debug("ObjectService::save::{0}".format(object_name))
        assert isinstance(data, dict)

        properties = self.get_properties(data)
        self.check_access(user, object_name, properties, AccessType.INSERT, True)

        self.create_access_log(db, user, object_name, AccessType.INSERT)

        data['createtime'] = str(datetime.datetime.now())
        data['owner'] = str(user.get("_id"))

        preprocessor_list = get_operation_preprocessor(object_name, AccessType.INSERT)
        for preprocessor in preprocessor_list:
            preprocessor(object_name, data, AccessType.INSERT)

        db[object_name].insert(data, callback=callback)

    def find(self, user, db, object_name, query, columns, callback, limit=5000):
        logging.debug("ObjectService::find::{0}".format(object_name))
        assert inspect.ismethod(callback)

        allowed_access_type =  self.check_access(user, object_name, columns, AccessType.READ, True)

        if allowed_access_type == ACCESS_TYPE_OWNER_ONLY:
            if query:
                assert isinstance(query, dict)
                query["owner"] = str(user.get("_id"))
            else:
                query = {"owner": str(user.get("_id"))}

        self.create_access_log(db, user, object_name, AccessType.READ)

        if len(columns) > 0:
            columns_dict = {column:1 for column in columns}
        else:
            columns_dict = None

        preprocessor_list = get_operation_preprocessor(object_name, AccessType.READ)
        for preprocessor in preprocessor_list:
            preprocessor(object_name, query, AccessType.READ)

        db[object_name].find(query, columns_dict).limit(limit).to_list(limit, callback)

    def load(self, user, db, object_name, id, columns, callback):
        logging.debug("ObjectService::load::{0}".format(object_name))
        assert inspect.ismethod(callback)

        allowed_access_type = self.check_access(user, object_name, columns, AccessType.READ, True)

        if len(columns) > 0:
            columns_dict = {column:1 for column in columns}
        else:
            columns_dict = None

        query = {'_id': ObjectId(id)}

        if allowed_access_type == ACCESS_TYPE_OWNER_ONLY:
            query["owner"] = str(user.get("_id"))

        self.create_access_log(db, user, object_name, AccessType.READ)

        preprocessor_list = get_operation_preprocessor(object_name, AccessType.READ)
        for preprocessor in preprocessor_list:
            preprocessor(object_name, query, AccessType.READ)

        db[object_name].find_one(query, columns_dict, callback=callback)

    def update(self, user, db, object_name, id, data, callback):
        logging.debug("ObjectService::update::{0}".format(object_name))
        assert len(id) > 0
        assert isinstance(data, dict)
        assert inspect.ismethod(callback)

        properties = self.get_properties(data)

        allowed_access_type = self.check_access(user, object_name, properties, AccessType.UPDATE, True)

        query = {'_id': ObjectId(id)}
        if allowed_access_type == ACCESS_TYPE_OWNER_ONLY:
            query["owner"] = str(user.get("_id"))

        self.create_access_log(db, user, object_name, AccessType.UPDATE)

        data['modifytime'] = str(datetime.datetime.now())

        preprocessor_list = get_operation_preprocessor(object_name, AccessType.UPDATE)
        for preprocessor in preprocessor_list:
            preprocessor(object_name, data, AccessType.UPDATE)

        db[object_name].update(query, {'$set': data}, callback=callback)

    def delete(self, user, db, object_name, id, callback):
        logging.debug("ObjectService::delete::{0}".format(object_name))
        assert len(id) > 0
        assert inspect.ismethod(callback)

        allowed_access_type = self.check_access(user, object_name, [], AccessType.DELETE, True)

        query = {'_id': ObjectId(id)}
        if allowed_access_type == ACCESS_TYPE_OWNER_ONLY:
            query["owner"] = str(user.get("_id"))

        self.create_access_log(db, user, object_name, AccessType.DELETE)

        preprocessor_list = get_operation_preprocessor(object_name, AccessType.DELETE)
        for preprocessor in preprocessor_list:
            preprocessor(object_name, None, AccessType.DELETE)

        db[object_name].remove(query, callback=callback)

    def get_properties(self, data, namespace=None):
        properties = data.keys()
        child_props = []

        for prop in properties:
            prop_data = data.get(prop, None)

            if prop_data and isinstance(prop_data, dict):
                child_namespace = (namespace + "." + prop) if namespace else prop
                child_props = child_props + self.get_properties(prop_data, child_namespace)

        if child_props:
            properties = properties + child_props

        properties = [p if not namespace else namespace + "." + p for p in properties]

        return properties

    def create_access_log(self, db, user, module, function):
        username = None
        access_log = {"username":username, 'module': module, 'function': function}
        access_log['createtime'] = str(datetime.datetime.now())
        #db.audit.access_log.insert(access_log, callback=None)


_preprocessors = {
}

def add_operation_preprocessor(preprocessor, object_name, access_types):
    #assert inspect.ismethod(preprocessor)
    assert isinstance(access_types, collections.Iterable)

    assert len(object_name) > 0

    object_preprocessor =_preprocessors.get(object_name)
    if not object_preprocessor:
        object_preprocessor = {}
        _preprocessors[object_name] = object_preprocessor

    for access_type in access_types:
        object_acctyp_preprocessor = object_preprocessor.get(access_type)
        if not object_acctyp_preprocessor:
            object_acctyp_preprocessor = []
            object_preprocessor[access_type] = object_acctyp_preprocessor

        if not preprocessor in object_acctyp_preprocessor:
            object_acctyp_preprocessor.append(preprocessor)

def get_operation_preprocessor(object_name, access_type):
    assert len(object_name) > 0
    object_preprocessor =_preprocessors.get(object_name)

    if not object_preprocessor:
        return []

    preprocessor_list = object_preprocessor.get(access_type)
    if not preprocessor_list:
        return []

    return preprocessor_list




