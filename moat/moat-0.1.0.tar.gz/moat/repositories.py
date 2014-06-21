
class Repository(object):

    def has_permission(self, permission, user, resource):
        raise NotImplementedError('Repository must implement has_permission')

    def set_permission(self, permission, user, resource):
        raise NotImplementedError('Repository must implement set_permission')

    def remove_permission(self, permission, user, resource):
        raise NotImplementedError(
            'Repository must implement remove_permission')

    def all_permissions(self, permission, user, resource_type):
        raise NotImplementedError('Repository must implement all_permissions')


class MockRepository(Repository):

    def __init__(self):
        self.permissions = {
            1: {
                1: {
                    'read': True,
                    'write': False,
                },
                2: {
                    'read': True,
                    'write': False,
                }
            }
        }

    def has_permission(self, permission, user, resource):
        return self.permissions[user.identifier()][resource.identifier()][permission.name]

    def set_permission(self, permission, user, resource):
        self.permissions[user.identifier()][resource.identifier()][
            permission.name] = True
        return True

    def remove_permission(self, permission, user, resource):
        if self.has_permission(permission, user, resource) is False:
            return False

        self.permissions[user.identifier()][resource.identifier()][
            permission.name] = False
        return True

    def all_permissions(self, permission, user, resource_type):
        ids = []

        for id, resource in self.permissions[1].items():
            print resource
            if resource[permission.name] is True:
                ids.append(id)

        return ids
