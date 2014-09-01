#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


#===============================================================================
# DOCS
#===============================================================================

"""http server for querying using qbj or yql

"""

#===============================================================================
# IMPORTS
#===============================================================================

import json, string, os

import jsonschema

import flask

from yatel import db, qbj


#===============================================================================
# CONSTANTS
#===============================================================================

#: JSON schema to validate configuration
CONF_SCHEMA = {
    "schema": "yatel server configuration schema",
    "type": "object",
    "properties": {
        "CONFIG": {
            "type": "object",
            "properties": {
                "DEBUG": {"type": "boolean"}
            },
            "additionalProperties": True
        },
        "NETWORKS": {
            "type": "object",
            "patternProperties": {
                "^[a-zA-Z0-9_-]$": {
                    "type": "object",
                    "properties":{
                        "uri": {"type": "string"},
                        "qbj": {"type": "boolean"}
                    },
                    "additionalProperties": False
                }
            }
        }
    }
}

CONF_BASE = {
    "CONFIG": {
        "DEBUG": True
    },
    "NETWORKS": {
        "network-name": {
            "uri": "uri",
            "qbj": True,
        }
    }
}

#: Template for WSGI configuration
WSGI_BASE_TPL = string.Template("""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, json

# Changes working directory so relative paths (and template lookup) work again
sys.path.append(os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))

# Error output redirect to Apache2 logs
sys.stdout =  sys.stderr

with open("${confpath}") as fp:
    conf = json.load(fp)

from yatel import server
application = server.from_dict(conf)

""")



#===============================================================================
# BASE CLASS
#===============================================================================

class YatelHttpServer(flask.Flask):
    """
    """

    def __init__(self, **config):
        super(YatelHttpServer, self).__init__(__name__)
        self.config.from_object(config)
        self._nws = {}
        self.route("/", methods=["POST", "GET"])(self.its_works)
        self.route("/qbj/<nwname>", methods=["POST", "GET"])(self.qbj)

    def add_nw(self, nwname, nw, enable_qbj):
        if not isinstance(nw, db.YatelNetwork):
            raise TypeError("nw must be db.YatelNetwork subclass")
        self._nws[nwname] = {"nwname": nwname, "nw": nw}
        if enable_qbj:
            self._nws[nwname]["qbj"] = qbj.QBJEngine(nw)

    def its_works(self):
        return flask.jsonify({type(self).__name__: "Works"})

    def qbj(self, nwname):
        qbj_nw = self._nws[nwname]["qbj"]
        response = qbj_nw.execute(
            flask.request.json, stacktrace=self.config["DEBUG"]
        )
        return flask.jsonify(response)

    def nw(self, name):
        return self._nws[name]["nw"]


#==============================================================================
# FUNCTIONS
#==============================================================================

def validate_conf(confdata):
    """Validates that the configuration structure given as JSON is correct.
    
    """
    return jsonschema.validate(confdata, CONF_SCHEMA)


def from_dict(data):
    """Returns a server created with a dictionary as configuration.
    
    """
    validate_conf(data)
    config = data["CONFIG"]
    server = YatelHttpServer(**config)
    for nwname, nwdata in data["NETWORKS"].items():
        nw = db.YatelNetwork(**db.parse_uri(nwdata["uri"]))
        qbj = nwdata.get("qbj", False)
        server.add_nw(nwname, nw, qbj)
    return server


def get_conf_template():
    """Returns a JSON configuration template as a String.
    
    """
    return json.dumps(CONF_BASE, indent=2)


def get_wsgi_template(confpath):
    """Returns WSGI configuration template as a String.
    
    Parameters
    ----------
    confpath: string
        Path to configuration file.
    
    """
    if not os.path.isfile(confpath):
        raise ValueError("confpath '{}' not exists".format(confpath))
    return WSGI_BASE_TPL.substitute(confpath=confpath).strip()



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)




