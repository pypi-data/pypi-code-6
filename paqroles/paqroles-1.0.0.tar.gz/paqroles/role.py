class Role:
    def __init__(self, name, permissions=[]):
        self.name = name
        self.permissions = permissions


    def __add__(self, other):
        return Role(self.name, self.permissions + other.permissions)


    def __radd__(self, other):
        return Role(other.name, other.permissions + self.permissions)


    def allows(self, permission, user=None, model=None, with_filters=True):
        for p in self.permissions:
            result = p.allows(permission, user, model, with_filters)
            if result is True or result is False:
                return result
        return False
