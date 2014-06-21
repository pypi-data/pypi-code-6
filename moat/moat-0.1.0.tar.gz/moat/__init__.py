from enum import Enum


class Permission(Enum):
    read = 'read'
    write = 'write'


class Moat(object):

    def __init__(self, repository):
        self.repository = repository

    def has(self, permission, user, resource):
        assert isinstance(permission, Permission)
        assert isinstance(user, UserMixin)
        assert isinstance(resource, ResourceMixin)

        return self.repository.has_permission(permission, user, resource)

    def set(self, permission, user, resource):
        assert isinstance(permission, Permission)
        assert isinstance(user, UserMixin)
        assert isinstance(resource, ResourceMixin)

        return self.repository.set_permission(permission, user, resource)

    def remove(self, permission, user, resource):
        assert isinstance(permission, Permission)
        assert isinstance(user, UserMixin)
        assert isinstance(resource, ResourceMixin)

        return self.repository.remove_permission(permission, user, resource)

    def all(self, permission, user, resource_type):
        assert isinstance(permission, Permission)
        assert isinstance(user, UserMixin)
        assert isinstance(resource_type, object)

        return self.repository.all_permissions(permission, user, resource_type)


class UserMixin(object):

    def identifier(self):
        raise NotImplementedError('User must implement identifier')


class ResourceMixin(object):

    def identifier(self):
        raise NotImplementedError('Resource must implement identifier')

    def type(self):
        raise NotImplementedError('Resource must implement type')
