__author__ = 'thunder'

from bson.objectid import ObjectId

from thunderargs import Arg


TYPECOMP = {'StringField': str,
            'IntField': int,
            'BooleanField': bool,
            'EmailField': str,
            'FloatField': float,
            'LongField': int,
            'ObjectIdField': ObjectId}


def field_to_arg(field):
    field_type = type(field).__name__
    multiple = False

    if field_type == 'ListField':

        field = field.field

        multiple = True


    return Arg(p_type=TYPECOMP.get(field_type, str),
               default=field.default,
               required=field.required,
               multiple=multiple)


def mongoengine_document_to_structure(model, with_pk=False):

    """
    Автоматически создаёт структуру данных по классу mongoengine document
    Если нужен ключ во входящих данных - юзай with_pk

    Эта функция формирует структуру аргументов для POST и PUT запросов
    """

    structure = {}
    pk = None
    for field in model._fields.values():
        if field.primary_key:
            pk = field.name

        else:
            structure[field.name] = field_to_arg(field)

    if with_pk:

        if not pk:
            pk = 'id'

        structure[pk] = field_to_arg(model._fields[pk])

    return structure




from mongoengine import Document
from thunderargs.endpoint import Endpoint
from thunderargs.validfarm import val_gt, val_lt
from .inherited_args import IntArg


def check_ancestor(base_cls):

    def wrapper(func):

        def wrapped(cls, *args, **kwargs):

            if isinstance(cls, base_cls):
                raise TypeError("class %s is not inherited by Document")

            return func(cls, *args, **kwargs)
        return wrapped
    return wrapper


@check_ancestor(Document)
def make_default_getlist(cls, to_str=True, name="default_getter_name"):

    @Endpoint
    def get(offset: IntArg(min_val=0, default=0),
            limit: IntArg(min_val=1, max_val=50, default=20)):
        resp = cls.objects.skip(offset).limit(limit)
        if to_str:
            return str(resp)

        return resp

    get.__name__ = name

    return get

@check_ancestor(Document)
def make_default_serializable_getlist(cls, name="default_getter_name"):

    @Endpoint
    def get(offset: IntArg(min_val=0, default=0),
            limit: IntArg(min_val=1, max_val=50, default=20)):
        return list(map(lambda x: x.get_serializable_dict(), cls.objects.skip(offset).limit(limit)))

    get.__name__ = name

    return get


from thunderargs.endpoint import annotate


@check_ancestor(Document)
def make_default_post(cls):

    structure = mongoengine_document_to_structure(cls)

    @Endpoint
    @annotate(**structure)
    def post(**kwargs):
        return str(cls(**kwargs).save().id)

    return post


@check_ancestor(Document)
def make_default_put(cls):

    structure = mongoengine_document_to_structure(cls, True)

    @Endpoint
    @annotate(**structure)
    def put(**kwargs):
        return cls(**kwargs).save(id)

    return put