"""
Kaiju is a framework created out of necessity to organize and build a
common interface to lots of standalone scripts and different kinds of data
analysis.

It saves a log of the operations used into MongoDB, as explained in the README.
There's also a command line interface which exposes all the operations defined.

"""

from bson.errors import InvalidDocument
from datetime import datetime
from functools import wraps
from inspect import getargspec
from pymongo import MongoClient
import sys


class KaijuException(Exception):
    pass


class FakeDatabase(object):
    def __getitem__(self, _):
        raise KaijuException("Kaiju application not connected to database.")


class Kaiju(object):
    LOG_COLLECTION = "kaiju_log"
    VAR_COLLECTION = "kaiju_var"

    def __init__(self, database_name):
        self.database_name = database_name
        self.database = FakeDatabase()

        self.operations = {}

        self.reset_flags()

    def reset_flags(self):
        self.allow_memoize = True
        self.allow_store = True

    def handle_kaiju_arguments(self, gargs):
        self.connect_database(gargs["database_uri"])

        self.reset_flags()
        self.enable_print = gargs["enable_print"]
        if gargs["no_memo"]:
            self.set_no_memo()
        if gargs["no_store"]:
            self.set_no_store()

    def connect_database(self, database_uri=None):
        self.mongo_client = MongoClient(database_uri)
        self.database = self.mongo_client[self.database_name]

        self.database[self.VAR_COLLECTION].ensure_index("name", 1)
        self.database[self.LOG_COLLECTION].ensure_index("date", 1)
        self.database[self.LOG_COLLECTION].ensure_index("operation", 1)

        for operation in self.operations.values():
            kaiju_parameters = operation.__kaiju__
            if "output" in kaiju_parameters:
                self.database[kaiju_parameters["output"]].ensure_index("maker_id", 1)

    def set_no_memo(self):
        self.allow_memoize = False

    def set_no_store(self):
        self.allow_store = False

    def __call__(self, **kaiju_parameters):
        def decorator(operation):
            @wraps(operation)
            def wrapper(*args, **kwargs):
                dictified_input_args = self.get_dictified_input_args(
                    operation, kaiju_parameters, args, kwargs
                )

                ## If operation has been executed previously, return
                ## stored result. Proceed with execution otherwise.
                if self.allow_memoize and self.allow_store:
                    existing_log_entry = self.log_query(operation.__name__, dictified_input_args)
                    if existing_log_entry is not None:
                        return existing_log_entry["_id"]

                if self.enable_print:
                    self.stdout_backup = sys.stdout
                    sys.stdout = sys.stderr

                new_kwargs = self.process_operation_args(
                    operation, kaiju_parameters, args, kwargs
                )

                result = operation(**new_kwargs)

                if self.enable_print:
                    sys.stdout = self.stdout_backup

                if "output" in kaiju_parameters and self.allow_store:
                    maker_id = self.log_add(
                        operation.__name__,
                        dictified_input_args,
                        kaiju_parameters["output"]
                    )
                    try:
                        self.store(kaiju_parameters["output"], result, maker_id)
                    except Exception:
                        self.delete(maker_id)
                        raise
                    return maker_id
                else:
                    return result

            wrapper.__original__ = operation
            wrapper.__kaiju__ = kaiju_parameters

            self.operations[operation.__name__] = wrapper
            return wrapper
        return decorator

    def execute(self, operation_name, kwargs):
        return self.operations[operation_name](**kwargs)

    def fetch(self, maker_id, collection=None, mongo_cursor=False):
        """Get documents from `collection` according to `maker_id`."""

        if collection is None:
            collection = self.database[self.LOG_COLLECTION].find_one(
                {"_id": maker_id}
            )["output"]

        query = self.database[collection].find({"maker_id": maker_id})
        if not mongo_cursor:
            return (x["value"] for x in query)
        else:
            return query

    def count(self, maker_id):
        """Count documents from `collection` according to `maker_id`."""

        return self.fetch(maker_id, mongo_cursor=True).count()

    def log_add(self, operation_name, kwargs, output_collection):
        return self.database[self.LOG_COLLECTION].insert(
            {
                "operation": operation_name,
                "kwargs": kwargs,
                "date": datetime.utcnow(),
                "output": output_collection
            }
        )

    def log_query(self, operation_name, kwargs):
        query = self.database[self.LOG_COLLECTION].find(
            {
                "operation": operation_name,
                "kwargs": kwargs
            }
        ).sort("date", -1).limit(1)
        query = list(query)
        return query[0] if query else None

    def log_find(self, *args, **kwargs):
        return self.database[self.LOG_COLLECTION].find(
            *args, **kwargs
        )

    def store(self, output_collection, data, maker_id):
        self.database[output_collection].insert(
            {
                "maker_id": maker_id,
                "value": x
            }
            for x in data
        )

    def delete(self, maker_id):
        run = self.database[self.LOG_COLLECTION].find_one({"_id": maker_id})
        if run is None:
            return False

        output_collection = run["output"]

        del_data = self.database[output_collection].remove({"maker_id": maker_id})["err"]
        del_log = self.database[self.LOG_COLLECTION].remove({"_id": maker_id})["err"]
        return (del_data is None and del_log is None)

    def fetch_log(self, operation_id=None):
        if operation_id is None:
            return self.database[self.LOG_COLLECTION].find().sort([("date", -1)]).limit(1000)
        else:
            return self.database[self.LOG_COLLECTION].find_one({"_id": operation_id})

    def drop_database(self):
        self.mongo_client.drop_database(self.database_name)

    def get_dictified_input_args(self, operation, kaiju_parameters, args, kwargs):
        operation_args = getargspec(operation)[0]

        dictified_input_args = {}
        dictified_input_args.update(kwargs)
        dictified_input_args.update(zip(operation_args, args))
        return dictified_input_args

    def process_operation_args(self, operation, kaiju_parameters, args, kwargs):
        operation_args = getargspec(operation)[0]

        new_kwargs = {
            k: (kaiju_parameters[k].process(self, v)
                if k in kaiju_parameters else v)
            for k, v in kwargs.items()
        }
        new_kwargs.update(
            {
                k: (kaiju_parameters[k].process(self, v)
                    if k in kaiju_parameters else v)
                for k, v in zip(operation_args, args)
            }
        )
        return new_kwargs

    def var_set(self, name, value):
        "Assign `value` to persitent variable `name`."

        if value is None:
            self.var_del(name)

        yield self.database[self.VAR_COLLECTION].update(
            {"name": name},
            {"name": name, "value": value},
            upsert=True
        )

    def var_del(self, name):
        yield self.database[self.VAR_COLLECTION].remove({"name": name})

    def var_get(self, name):
        query = self.database[self.VAR_COLLECTION].find_one({"name": name})
        yield query["value"] if query is not None else None

    def var_ls(self):
        return ({"name": x["name"], "value": x["value"]}
                for x in self.database[self.VAR_COLLECTION].find())
