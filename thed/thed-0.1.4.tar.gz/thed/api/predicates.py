from __future__ import unicode_literals


class ResourcePredicate(object):
    """
    """

    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'val=%s' % (self.val,)

    phash = text

    def __call__(self, context, request):
        return context.entity and isinstance(context.entity, self.val)
