#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# DOCS
#===============================================================================

"""Defines the schema to validate all incomming QBJ.

- http://www.tutorialspoint.com/json/json_schema.htm

"""

#===============================================================================
# IMPORTS
#===============================================================================

import jsonschema

from yatel.qbj import functions
from yatel import typeconv


#===============================================================================
# SCHEMA
#===============================================================================

# http://www.tutorialspoint.com/json/json_schema.htm


#: Extra definitions for the schema validation.
DEFINITIONS = {
    "TYPE_SINGLE_DEF" : {
        "type": "string",
        "enum": typeconv.NAMES_TO_TYPES.keys()
    },

    "TYPE_ARRAY_DEF" : {
        "type": "array",
        "items": {"$ref": "#/definitions/TYPE_DEF"},
    },

    "TYPE_OBJECT_DEF" : {
        "type": "object",
        "patternProperties": {
            r".*": {"$ref": "#/definitions/TYPE_DEF"}
        },
    },
    
    "TYPE_DEF" : {
        "oneOf": [
            {"$ref": "#/definitions/TYPE_SINGLE_DEF"},
            {"$ref": "#/definitions/TYPE_ARRAY_DEF"},
            {"$ref": "#/definitions/TYPE_OBJECT_DEF"},
            {"type": "string", "enum": ["literal", "iterable"]}
      ]
    },

    "ARGUMENT_STATIC_DEF": {
        "type": "object",
        "properties": {
            "type": {"$ref": "#/definitions/TYPE_DEF"},
            "value": {}
        },
        "additionalProperties": False,
        "required": ["type", "value"]
    },

    "ARGUMENT_FUNCTION_DEF": {
        "type": "object",
        "properties": {
            "type": {"$ref": "#/definitions/TYPE_DEF"},
            "function": {"$ref": "#/definitions/FUNCTION_DEF"}
        },
        "additionalProperties": False,
        "required": ["type", "function"]
    },

    "FUNCTION_DEF": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "enum": functions.FUNCTIONS.keys()},
            "args": {
                "type": "array",
                "items": {
                    "oneOf": [
                        {"$ref": "#/definitions/ARGUMENT_STATIC_DEF"},
                        {"$ref": "#/definitions/ARGUMENT_FUNCTION_DEF"}
                    ]
                }
            },
            "kwargs": {
                "type": "object",
                "patternProperties": {
                    r".*": {
                        "oneOf": [
                            {"$ref": "#/definitions/ARGUMENT_STATIC_DEF"},
                            {"$ref": "#/definitions/ARGUMENT_FUNCTION_DEF"}
                        ]
                    }
                },
            },
        },
        "required": ["name"],
        "additionalProperties": False
    }
}


#: Schema to validate QBJ queries.
QBJ_SCHEMA = {
    # metadata
    "title": "Yatel QBJ Schema",
    "description": __doc__,

    # validation itself
    "type":  "object",
    "definitions" : DEFINITIONS,
    "properties": {
        "id": {"type": ["string", "number", "boolean", "null"]},
        "function": { "$ref": "#/definitions/FUNCTION_DEF" }
    },
    "required": ["id", "function"],
    "additionalProperties": False,
}


#===============================================================================
# FUNCTION
#===============================================================================

def validate(to_validate, *args, **kwargs):
    """Validates that the query structure given as JSON is correct.
    
    Parameters
    ----------
        to_validate : str
            String in JSON format.
    
    Raises
    ------
        ValidationError
            When ``to_validate`` does not have the corresponding structure.

    """
    return jsonschema.validate(to_validate, QBJ_SCHEMA, *args, **kwargs)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
