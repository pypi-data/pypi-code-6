# TODO: add custom format validation for `date` and `timestamp`
# https://python-jsonschema.readthedocs.org/en/latest/validate/#validating-formats

import functools
import collections
import inspect
import json
import yaml
import jsonschema
import hashlib
import utils

def dictionary_sort(value, **kwargs):
    """ Recursive (a.k.a. deep) dictionary sort. """

    self = functools.partial(dictionary_sort, **kwargs)

    if isinstance(value, dict):
        items = zip(value.keys(), map(self, value.values()))
        order = sorted(items, **kwargs)
        return collections.OrderedDict(order)
    else:
        return value

def hash(schema):
    """ Return a unique identifier for a schema. """

    # Dictionaries are not sorted, meaning that to make sure 
    # that the same schema will always return the same hash, 
    # regardless of how exactly that schema was written down, 
    # we first need to sort the keys.
    sorted_schema = dictionary_sort(schema, key=utils.first)
    signature = hashlib.sha1(json.dumps(sorted_schema)).hexdigest()
    return signature

def validate(sign=False):
    """
    A validation decorator that will read a JSON schema from 
    the function's docstring and make sure the function follows
    the schema. Very useful for design by contract.

    The JSON schema can be specified in, you guessed it, JSON, but 
    it may also be written in YAML to cut down on the verbosity.

    A trivial example: 

        @validate
        def record(first, last, age):
            '''
            description: |
                Create a personnel record.
            type: object
            properties:
                required: [age]
                name:
                    type: object
                    required: [last]
                    properties:
                        first:
                            type: string
                        last:
                            type: string
                age:
                    type: number
            '''

            return {
                'name': {
                    'first': first, 
                    'last': last, 
                }, 
                'age': age, 
            }

    """

    def validation_decorator(fn):
        doc = inspect.getdoc(fn)
        schema = yaml.load(doc)

        @functools.wraps(fn)
        def validated_fn(*vargs, **kwargs):
            retval = fn(*vargs, **kwargs)
            jsonschema.validate(retval, schema)

            if sign:
                if isinstance(sign, basestring):
                    key = sign
                else:
                    key = 'schema'
                retval.update({key: hash(schema)})
            
            return retval

        # not strictly needed for anything, but it's useful to 
        # have the parsed schema available somewhere
        validated_fn.schema = schema

        return validated_fn

    return validation_decorator