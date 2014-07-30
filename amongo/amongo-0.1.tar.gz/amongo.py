from bson.son import SON
from pymongo.collection import Collection


class AMongoObject(object):
    def __init__(self, collection):
        self.collection = collection
        self.pipeline = []

    def execute(self):
        if self.pipeline:
            res = self.collection.aggregate(self.pipeline)
            if res['ok'] == 1:
                return res['result']
            else:
                raise Exception('MongoDb returned not OK')
        else:
            return self.collection.find()

    def group(self, by, add_count=False, **kwargs):
        group_stage = {}
        project_stage = {}

        group_stage['_id'] = {}

        if isinstance(by, basestring):
            by = (by, )

        if not by:
            group_stage['_id'] = None
        else:
            for key_part in by:
                if isinstance(key_part, basestring):
                    group_stage['_id'][key_part] = '$%s' % key_part
                    project_stage[key_part] = '$_id.%s' % key_part
                else:
                    raise Exception('Unsupported value in "by" parameter')

        if add_count is True:
            group_stage['count'] = {'$sum': 1}
            project_stage['count'] = True

        for k, v in kwargs.items():
            group_stage[k] = v
            project_stage[k] = True

        if '_id' not in project_stage:
            project_stage['_id'] = False

        self.pipeline.append({'$group': group_stage})
        self.pipeline.append({'$project': project_stage})
        return self

    def unwind(self, array_field=None, **kwargs):
        if array_field is not None and kwargs:
            raise Exception('Passing both array_field and keyword arguments is unsupported')
        if len(kwargs) > 1:
            raise Exception('Unwind on multiple fields not supported')
        self.pipeline.append({'$unwind': '$%s' % (array_field if array_field is not None else kwargs.keys()[0])})
        return self

    def project(self, **kwargs):
        self.pipeline.append({'$project': kwargs})
        return self

    def match(self, condition=None, **kwargs):
        if condition is not None and kwargs:
            raise Exception('Passing both condition and keyword arguments is unsupported')
        self.pipeline.append({'$match': kwargs if kwargs else condition})
        return self

    where = match

    def sort(self, *args, **kwargs):
        if len(kwargs) > 1:
            raise Exception('Passing multiple sort keys as keyword arguments not supported: order is lost this way')
        if kwargs and args:
            raise Exception('Passing keyword arguments as both keyword and positional argument is not supported')
        if not args and not kwargs:
            raise Exception('No sort key specified')

        if kwargs:
            by = kwargs.items()
        elif args:
            by = args

        presets = {True: 1, 'asc': 1, 'desc': -1}
        by = [(el, 1) if isinstance(el, basestring) else el for el in by]
        by = [(key, presets[d] if d in presets else d) for key, d in by]

        self.pipeline.append({'$sort': SON(by)})
        return self

    def limit(self, count, skip=None):
        if skip is not None:
            self.pipeline.append({'$skip': skip})
        self.pipeline.append({'$limit': count})
        return self

    def skip(self, count):
        self.pipeline.append({'$skip': count})
        return self


Collection.a = property(lambda coll: AMongoObject(coll))


for _ in [1]:  # not to clutter global scope
    def get_func(fname):
        def func(expr):
            return {'$%s' % fname: '$%s' % expr if isinstance(expr, basestring) else expr}

        func.__name__ = fname
        return func

    for fname in ['addToSet', 'first', 'last', 'max', 'min', 'avg', 'push', 'sum']:
        closure_fname = fname[:]
        globals()['%s_' % fname] = get_func(fname)


for _ in [1]:  # not to clutter global scope
    def get_func(fname):
        def func(expr_a, expr_b):
            return {'$%s' % fname: [expr_a, expr_b]}

        func.__name__ = fname
        return func

    for fname in ['and', 'or', 'cmp', 'eq', 'gt', 'gte', 'lt', 'lte', 'ne']:
        closure_fname = fname[:]
        globals()['%s_' % fname] = get_func(fname)