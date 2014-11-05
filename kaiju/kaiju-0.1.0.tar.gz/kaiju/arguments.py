import re

from bson.json_util import loads
import bson.objectid  # For BSON's ObjectId.


class Argument(object):

    def __init__(self, **extra_config):
        self.config = dict(extra_config)
        if self.parse:
            self.config["type"] = self.parse

    def parse(self, string):
        return string

    def process(self, app, value):
        return value


class Var(Argument):

    def parse(self, string):
        try:
            return loads(string)
        except ValueError:
            raise ValueError(
                "Cannot deserialize argument: \"{}\". Maybe it is a string missing quotes?"
                .format(string)
            )


class File(Argument):

    def __init__(self, mode="r", **extra_config):
        super(File, self).__init__(**extra_config)
        self._mode = mode

    def process(self, app, value):
        return open(value, mode=self._mode) if value is not None else None


class DictsFile(Argument):
    """A "dicts file" is a text file that containts a JSON-coded
dictionary in each line. Similar to a MongoDB collection of documents,
each line from the file is a document.

    """

    def process(self, app, value):
        return (loads(x) for x in open(value))


class Data(Argument):

    def __init__(self, collection, mongo_cursor=False, **extra_config):
        super(Data, self).__init__(**extra_config)
        self._collection = collection
        self.collection = collection
        self.mongo_cursor = mongo_cursor

    def parse(self, value):
        return oid_parser(value)

    def process(self, app, value):
        return app.fetch(value, collection=self._collection, mongo_cursor=self.mongo_cursor)


class ObjectId(Argument):

    def __init__(self, **extra_config):
        super(ObjectId, self).__init__(**extra_config)

    def parse(self, value):
        return oid_parser(value)


class RawString(Argument):
    pass


class Int(Argument):

    def parse(self, value):
        return int(value)


class Float(Argument):

    def parse(self, value):
        return float(value)


class Bool(Var):

    def __init__(self, action="store_true", **extra_config):
        super(Bool, self).__init__(action=action, **extra_config)

    parse = None


def oid_parser(value):
    """
    Parse a `value` representing a MongoDB ObjectID.

    The parameter `value` can be a JSON string, e.g. `{'$oid': '...'}`, or a
    24-digit hexadecimal value.
    """
    m = re.match("[a-fA-F0-9]{24}", value)

    if m is not None:  # RegExp matched: it's a hexadecimal string.
        return bson.objectid.ObjectId(value)
    else:  # Check if it's a JSON string.
        msg = "Couldn't parse given string as an ObjectId."
        assert type(loads(value)) == bson.objectid.ObjectId, msg

        return loads(value)
