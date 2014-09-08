import copy
import functools

from paqroles.mask import Mask


def clones(func):
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        clone = copy.deepcopy(self)
        func(clone, *args, **kwargs)
        return clone
    return inner


class Permission:
    def __init__(self, mask='', filters=[], inverse=False):
        self.mask = Mask(mask)
        self.filters = filters.copy()
        self.inverse = inverse


    @clones
    def __call__(self, next_part):
        if callable(next_part):
            self.filters.append(next_part)
        else:
            self.mask += Mask(next_part)


    def __invert__(self):
        self.inverse = True
        return self


    def allows(self, mask, user=None, model=None, with_filters=True):
        mask = Mask(mask)
        filters = self.filters if with_filters else []
        if self.inverse:
            return False if self.mask.allows(mask) else None
        else:
            if self.mask.allows(mask):
                if user and model:
                    for func in filters:
                        if not func(user, model):
                            return None
                    return True
                elif user:
                    for func in filters:
                        try:
                            if not func(user):
                                return None
                        except Exception:
                            return None
                    return True
                else:
                    return not bool(filters)
            else:
                return None


    @clones
    def own(self, field='user'):
        self.filters.append(factory_is_own(field))


class SuperPermission(Permission):
    def allows(self, mask, user=None, model=None, filters=[]):
        return not self.inverse