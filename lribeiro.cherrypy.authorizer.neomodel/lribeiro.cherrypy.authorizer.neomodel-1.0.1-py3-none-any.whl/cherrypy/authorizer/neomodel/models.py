import datetime

import bcrypt
from neomodel import StructuredNode, StructuredRel, StringProperty, DateTimeProperty, RelationshipFrom, RelationshipTo


class PermissionRel(StructuredRel):
    action = StringProperty(required=True)


class Resource(StructuredNode):
    name = StringProperty(required=True, unique_index=True)
    permissions = RelationshipFrom('User', 'HAS_PERMISSION', PermissionRel)


class User(StructuredNode):
    email = StringProperty(required=True, unique_index=True)
    password = StringProperty()
    name = StringProperty()
    created_at = DateTimeProperty(default=datetime.datetime.now)
    modified_at = DateTimeProperty()

    permissions = RelationshipTo(Resource, 'HAS_PERMISSION', model=PermissionRel)

    def set_password(self, plain_password: str):
        hashed = bcrypt.hashpw(bytes(plain_password, 'utf-8'), bcrypt.gensalt())
        self.password = bytes.decode(hashed, 'utf-8')