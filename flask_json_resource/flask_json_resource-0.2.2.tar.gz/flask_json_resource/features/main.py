from flask import Flask
from flask.ext.pymongo import PyMongo
from flask.ext.json_resource import API
from json_resource import Schema


app = Flask('test')
db = PyMongo(app)
api = API('flask_json_resource.features.steps')


@api.register()
class Message(api.Resource):
    schema = Schema({'id': 'message'})


@api.register()
class MessageCollection(api.Collection):
    schema = Schema({'id': 'message-collection'})
    objects = Message.objects


api.init_app(app, db)
