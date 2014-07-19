__author__ = 'thunder'

from bson.objectid import ObjectId

from thunderargs import Arg

class ItemArg(Arg):
    """
    use it with mongoengine
    """

    def __init__(self, collection, **kwargs):
        kwargs['p_type'] = ObjectId
        kwargs['expander'] = lambda x: collection.objects.get(pk=x)
        super().__init__(**kwargs)


def make_itemarg_class(collection):
    class ItemArg(Arg):

        def __init__(self, **kwargs):
            kwargs['p_type'] = ObjectId
            kwargs['expander'] = lambda x: collection.objects.get(pk=x)
            super().__init__(**kwargs)

    return ItemArg