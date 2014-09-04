import datetime

import bcrypt
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import \
    StringField, ListField, ReferenceField, EmbeddedDocumentField, DateTimeField, EmailField


class Resource(Document):
    name = StringField(required=True, unique=True)


class Permission(EmbeddedDocument):
    action = StringField(required=True, unique_with='resource')
    resource = ReferenceField(Resource)


class User(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(max_length=255)
    name = StringField(max_length=100)
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField()

    permissions = ListField(EmbeddedDocumentField(Permission))

    def set_password(self, plain_password: str):
        hashed = bcrypt.hashpw(bytes(plain_password, 'utf-8'), bcrypt.gensalt())
        self.password = bytes.decode(hashed, 'utf-8')

    meta = {
        'allow_inheritance': True,
        'indexes': ['email', 'name']
    }