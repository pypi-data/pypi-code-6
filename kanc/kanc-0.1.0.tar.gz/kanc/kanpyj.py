# Copyright (C) 2014 Yuichi Murata
# https://github.com/yuichi1004/kanc
# https://github.com/yuichi1004/tiny-pyj
import re
import json
import urllib2
import urllib
import base64

class RpcMethod(object):
    def __init__(self, client, method, service):
        self.service = service 
        self.method = method
        self.client = client
    def __call__(self, *args, **kwargs):
        return self.client.request(self.method, self.service, args, kwargs)

class RpcError(Exception): 
    def __init__(self, msg):
        super(RpcError, self).__init__(msg)

class RpcValidationError(RpcError): 
    def __init__(self, msg):
        super(RpcValidationError, self).__init__(msg)

class ClientBase(object):
    def __init__(self, smd, host, username = None, password = None):
        self.req_id = 0
        self.smd = smd
        self.host = host
        self.username = username
        self.password = password
        self.strict_validation = True
        self.services = smd['services']
        for s in self.services:
            method_name = re.sub('([A-Z])', r'_\1', s).lower()
            setattr(self, method_name, RpcMethod(self, s, self.services[s]))
        
        self.url_opener = urllib2.build_opener()
        if username is not None and password is not None:
            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(None, self.host, username, password)
            auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            self.url_opener = urllib2.build_opener(auth_handler)
    
    def validate_param(self, name, value, type):
        if value is None:
            return

        if (self.strict_validation):
            # Perform strict validation. Error if type not matched
            if (type == 'integer'):
                if not isinstance(value, int):
                    raise RpcValidationError('{} needs to be integer'.format(name))
            if (type == 'string'):
                if not isinstance(value, str):
                    raise RpcValidationError('{} needs to be string'.format(name))
            if (type == 'boolean'):
                if not isinstance(value, bool):
                    raise RpcValidationError('{} needs to be boolean'.format(name))
        else:
            # Perform non-strict validation. Error if value cannot be cast
            if (type == 'integer'):
                try:
                    int(value)
                except ValueError:
                    raise RpcValidationError('{} needs to be integer'.format(name))
            if (type == 'string'):
                try:
                    str(value)
                except ValueError:
                    raise RpcValidationError('{} needs to be string'.format(name))
            if (type == 'boolean'):
                try:
                    bool(value)
                except ValueError:
                    raise RpcValidationError('{} needs to be boolean'.format(name))

    def cast_param(self, name, value, type):
        if (type == 'integer'):
            return int(value)
        if (type == 'string'):
            return str(value)
        if (type == 'boolean'):
            return bool(value)
        return value

    def request(self, method, service, args, kwargs):
        unchecked_args = kwargs
        checked_args = {}
        parameters = service['parameters']
        for i in range(0, len(args)):
            name = parameters[i]['name']
            unchecked_args[name] = args[i]
        for p in parameters:
            name = p['name']
            if unchecked_args.has_key(name):
                if unchecked_args[name] is not None:
                    self.validate_param(name, unchecked_args[name], p['type'])
                    v = self.cast_param(name, unchecked_args[name], p['type'])
                    checked_args[name] = v 
                del unchecked_args[name]
            else:
                if not p['optional']:
                    raise RpcError('arg {} is required'.format(name))
        if len(unchecked_args) > 0:
            raise RpcError('Unknown args: ' + str(unchecked_args))

        transport = self.smd['transport']
        if 'transport' in service:
            transport = service['transport']
        
        headers = {'content-type': 'application/json'}
        payload = {
            'method': method,
            'jsonrpc': '2.0',
            'id': self.req_id,
        }
        self.req_id = self.req_id + 1
        
        url = self.host + self.smd['target']
        req = None
        if transport == 'POST':
            if (checked_args is not None):
                payload['params'] = checked_args 
            payload = self.pre_request_send(payload)
            req = urllib2.Request(url, json.dumps(payload), headers)
        elif transport == 'GET':
            if (checked_args is not None):
                paramstr = json.dumps(checked_args)
                paramstr =  base64.b64encode(paramstr)
                payload['params'] = paramstr
            payload = self.pre_request_send(payload)
            query = urllib.urlencode(payload)
            req = urllib2.Request(url + '?' + query,
                    None, headers)
        else:
            raise RpcError('Unknown transport: ' + transport)
        resp = None
        try:
            resp = self.url_opener.open(req)
        except urllib2.URLError, e:
            resp = e
        j = json.loads(resp.read())
        if ('error' in j):
            raise RpcError(j['error'])
        return j['result']
    
    def pre_request_send(self, payload):
        """ Pre-processor for request payload
        Arguments:
        payload -- request payload to be sent
        
        Returns:
        Processed payload
        """
        return payload

smd = """
{
  "target": "/jsonrpc.php",
  "transport": "POST",
  "services": {
    "createProject": {
      "parameters": [
        {"name": "name", "type": "string", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "getProjectById": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "object"
      }
    },
    "getProjectByName": {
      "parameters": [
        {"name": "name", "type": "string", "optional": false}
      ],
      "returns": {
        "type": "object"
      }
    },
    "getAllProjects": {
      "parameters": [],
      "returns": {
        "type": "array"
      }
    },
    "updateProject": {
      "parameters": [
        {"name": "id", "type": "integer", "optional": false}, 
        {"name": "name", "type": "string", "optional": false}, 
        {"name": "is_active", "type": "integer", "optional": true}, 
        {"name": "token", "type": "string", "optional": true}, 
        {"name": "is_public", "type": "integer", "optional": true}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "removeProject": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "enableProject": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "disableProject": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "enableProjectPublicAccess": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "disableProjectPublicAccess": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false} 
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "getAllowedUsers": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "object"
      }
    },
    "allowUser": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}, 
        {"name": "user_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "revokeUser": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}, 
        {"name": "user_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "getColumns": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "array"
      }
    },
    "getColumn": {
      "parameters": [
        {"name": "column_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "object"
      }
    },
    "moveColumnUp": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}, 
        {"name": "column_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "moveColumnDown": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}, 
        {"name": "column_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "updateColumn": {
      "parameters": [
        {"name": "column_id", "type": "integer", "optional": false}, 
        {"name": "title", "type": "string", "optional": false}, 
        {"name": "task_limit", "type": "integer", "optional": true}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "addColumn": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}, 
        {"name": "title", "type": "string", "optional": false}, 
        {"name": "task_limit", "type": "integer", "optional": true}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "removeColumn": {
      "parameters": [
        {"name": "column_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "createTask": {
      "parameters": [
        {"name": "title", "type": "string", "optional": false}, 
        {"name": "project_id", "type": "integer", "optional": false}, 
        {"name": "color_id", "type": "string", "optional": true}, 
        {"name": "column_id", "type": "integer", "optional": true}, 
        {"name": "description", "type": "string", "optional": true}, 
        {"name": "owner_id", "type": "integer", "optional": true}, 
        {"name": "creator_id", "type": "integer", "optional": true}, 
        {"name": "score", "type": "integer", "optional": true}, 
        {"name": "date_due", "type": "string", "optional": true}, 
        {"name": "category_id", "type": "integer", "optional": true}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "updateTask": {
      "parameters": [
        {"name": "id", "type": "integer", "optional": false}, 
        {"name": "title", "type": "string", "optional": true}, 
        {"name": "color_id", "type": "string", "optional": true}, 
        {"name": "project_id", "type": "integer", "optional": true}, 
        {"name": "column_id", "type": "integer", "optional": true}, 
        {"name": "description", "type": "string", "optional": true}, 
        {"name": "owner_id", "type": "integer", "optional": true}, 
        {"name": "creator_id", "type": "string", "optional": true}, 
        {"name": "score", "type": "integer", "optional": true}, 
        {"name": "date_due", "type": "string", "optional": true}, 
        {"name": "category_id", "type": "integer", "optional": true}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "openTask": {
      "parameters": [
        {"name": "task_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "closeTask": {
      "parameters": [
        {"name": "task_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "removeTask": {
      "parameters": [
        {"name": "task_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "moveTaskPosition": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}, 
        {"name": "task_id", "type": "integer", "optional": false}, 
        {"name": "column_id", "type": "integer", "optional": false}, 
        {"name": "position", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "getAllTasks": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}, 
        {"name": "status", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "array"
      }
    },
    "getTask": {
      "parameters": [
        {"name": "task_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "object"
      }
    },
    "createUser": {
      "parameters": [
        {"name": "username", "type": "string", "optional": false}, 
        {"name": "password", "type": "string", "optional": false}, 
        {"name": "name", "type": "string", "optional": true}, 
        {"name": "email", "type": "string", "optional": true}, 
        {"name": "is_admin", "type": "integer", "optional": true}, 
        {"name": "default_project_id", "type": "integer", "optional": true}
      ],
      "returns": {
        "type": "object"
      }
    },
    "updateUser": {
      "parameters": [
        {"name": "id", "type": "integer", "optional": false}, 
        {"name": "username", "type": "string", "optional": true}, 
        {"name": "name", "type": "string", "optional": true}, 
        {"name": "email", "type": "string", "optional": true}, 
        {"name": "is_admin", "type": "integer", "optional": true}, 
        {"name": "default_project_id", "type": "integer", "optional": true}
      ],
      "returns": {
        "type": "object"
      }
    },
    "removeUser": {
      "parameters": [
        {"name": "user_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "getUser": {
      "parameters": [
        {"name": "user_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "object"
      }
    },
    "getAllUsers": {
      "parameters": [
      ],
      "returns": {
        "type": "array"
      }
    },
    "createCategory": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "updateCategory": {
      "parameters": [
        {"name": "id", "type": "integer", "optional": false}, 
        {"name": "name", "type": "string", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "removeCategory": {
      "parameters": [
        {"name": "category_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "getCategory": {
      "parameters": [
        {"name": "category_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "object"
      }
    },
    "getAllCategory": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "array"
      }
    },
    "createComment": {
      "parameters": [
        {"name": "task_id", "type": "integer", "optional": false}, 
        {"name": "user_id", "type": "integer", "optional": false}, 
        {"name": "content", "type": "string", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "updateComment": {
      "parameters": [
        {"name": "id", "type": "integer", "optional": false}, 
        {"name": "content", "type": "string", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "getComment": {
      "parameters": [
        {"name": "comment_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "object"
      }
    },
    "removeComment": {
      "parameters": [
        {"name": "comment_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "getAllComments": {
      "parameters": [
        {"name": "task_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "array"
      }
    },
    "createSubtask": {
      "parameters": [
        {"name": "task_id", "type": "integer", "optional": false}, 
        {"name": "title", "type": "string", "optional": false}, 
        {"name": "assignee_id", "type": "integer", "optional": true}, 
        {"name": "time_estimated", "type": "integer", "optional": true}, 
        {"name": "time_spent", "type": "integer", "optional": true}, 
        {"name": "status", "type": "integer", "optional": true}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "updateSubtask": {
      "parameters": [
        {"name": "id", "type": "integer", "optional": false}, 
        {"name": "task_id", "type": "integer", "optional": false}, 
        {"name": "title", "type": "string", "optional": true}, 
        {"name": "assignee_id", "type": "integer", "optional": true}, 
        {"name": "time_estimated", "type": "integer", "optional": true}, 
        {"name": "time_spent", "type": "integer", "optional": true}, 
        {"name": "status", "type": "integer", "optional": true}
      ],
      "returns": {
        "type": "boolean"
      }
    },
    "removeSubtask": {
      "parameters": [
        {"name": "subtask_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "object"
      }
    },
    "getSubtask": {
      "parameters": [
        {"name": "subtask_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "object"
      }
    },
    "getAllSubtasks": {
      "parameters": [
        {"name": "task_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "array"
      }
    },
    "getBoard": {
      "parameters": [
        {"name": "project_id", "type": "integer", "optional": false}
      ],
      "returns": {
        "type": "array"
      }
    }
  }
}
"""

class Client(ClientBase):
    """
    Kanboard API client
    """
    def __init__(self, host, key):
        smd_json = json.loads(smd)
        super(Client, self).__init__(smd_json, host, 'jsonrpc', key)
        self.strict_validation = False
    
    def remove_unused_params(self, method, params):
        """ Remvoe unused parameters
        Arguments:
        method -- Method name
        params -- Given parameters

        Returns:
        Output parameters without unused params
        """
        checked_params = {}
        for s in self.smd['services']:
            if s == method:
                service = self.smd['services'][s]
                for p in service['parameters']:
                    name = p['name']
                    if name in params:
                        checked_params[name] = params[name]
        return checked_params

    def create_empty_params(self, method):
        """ Create parameters with empty values
        Arguments:
        method -- Method name

        Returns:
        empty parameter for the method 
        """
        params = {}
        for s in self.smd['services']:
            if s == method:
                service = self.smd['services'][s]
                for p in service['parameters']:
                    if p['type'] == 'object':
                        params[p['name']] = {}
                    elif p['type'] == 'string':
                        params[p['name']] = ""
                    else:
                        params[p['name']] = None
        return params
        

class PatchedClient(Client):
    """
    Kanboard API client with compatibility patch
    This is required for implementation bug of kanboard API
    """
    def __init__(self, host, key):
        super(PatchedClient, self).__init__(host, key)

    def pre_request_send(self, payload):
        if payload['method'] == 'getAllTasks':
            payload['params']['status'] = [payload['params']['status']]
        if payload['method'] == 'createUser':
            payload['params']['confirmation'] = payload['params']['password']
            payload['params'] = {'values': payload['params']}
        if payload['method'] == 'updateUser':
            payload['params'] = {'values': payload['params']}
        return payload

