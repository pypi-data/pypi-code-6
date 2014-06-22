# -*- coding: utf-8 -*-

from .fields import MsgFields as F


def build_schema(schema, add_meta=True, type_="object"):
    """
    Adds a few necessary embelishments to any schema
    """

    schema["$schema"] = "http://json-schema.org/draft-04/schema#"
    schema["type"] = type_
    schema["additionalProperties"] = False
    if add_meta:
        schema["properties"][F.META] = _MetaSchema
    return schema

_MetaSchema = build_schema({
    "properties": {
        F.META_START_TIME: {"type": "string"},
        F.META_END_TIME: {"type": "string"},
        F.META_VERSION: {"type": "string"},
        F.META_ERR: {"type": ["string", "null"]},
        F.META_MSG: {"type": ["string", "null"]},
    }
}, add_meta=False)

# TaskResultSet schema, currently not checked, but defined for completeness
TrsSchema = build_schema({
    "properties": {
        F.TRS_META_JOB_ID: {"type": "number"},
        F.TRS_META_TARGET_ID: {"type": "number"},
    }
}, add_meta=False)

TestSchema = build_schema({
    "properties": {
        "a": {"type": "string"},
        "b": {"type": ["string", "null"]},
        u"レスト": {"type": ["string", "null"]},
    },
    "required": ["a"]
})

# ############ Add schemas from here ################

ArtifactSchema = build_schema({
    "properties": {
        F.PATH: {"type": "string"},
    }
})

DomainSchema = build_schema({
    "properties": {
        F.DOMAIN: {"type": "string"},
    }
})

HostnameSchema = build_schema({
    "properties": {
        F.HOSTNAME: {"type": "string"},
    }
})

IpSingleSchema = build_schema({
    "properties": {
        F.IP: {
            "type": ["string", "null"],
        }
    }
}, add_meta=False)

IpsetSchema = build_schema({
    "properties": {
        F.IPSET: {
            "type": "array",
            "items": {
                "type": ["string", "null"],
                "format": "ipv4",
            }
        }
    }
})

GeoipSchema = build_schema({
    "properties": {
        F.GEOIP: {
            "type": "object",
            "patternProperties": {
                "^(\d{1,3}\.){1,3}(\d{1,3})$": {
                    "type": "object",
                    "properties": {
                        F.COUNTRY_CODE: {"type": ["string", "null"]},
                        F.LAT: {"type": ["number", "null"]},
                        F.LONG: {"type": ["number", "null"]},
                    }
                }
            },
            "additionalProperties": False,
        },
    }
})

HttpstatusSchema = build_schema({
    "properties": {
        F.HTTP_STATUS: {"type": ["number", "null"]},
    }
})

UrlSchema = build_schema({
    "properties": {
        F.URL: {"type": "string"},
    }
})

WhoisSchema = build_schema({
    "properties": {
        F.WHOIS_RAW: {"type": ["string", "null"]},
    }
})
