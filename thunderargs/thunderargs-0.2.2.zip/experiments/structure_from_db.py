__author__ = 'thunder'

from mongoengine import *

from thunderargs.endpoint import annotate, Endpoint
from .inherited_args import IntArg

TYPES = {'IntArg': IntArg}

connect('thunderargs_example')


class DBArg(Document):

    name = StringField(max_length=30, min_length=1, required=True)
    arg_type = StringField(default="IntArg")
    params = DictField()

    def get_arg(self):

        arg = TYPES[self.arg_type](**self.params)
        arg.db_entity = self

        return arg




class DBStruct(Document):

    args = ListField(ReferenceField(DBArg))

    def get_structure(self):
        return {x.name: x.get_arg() for x in self.args}



class Category(Document):

    name = StringField(primary_key=True)
    label = StringField()
    parent = ReferenceField('self')

    arg_structure = ReferenceField(DBStruct)


    def get_creator(self):

        @Endpoint
        @annotate(**self.arg_structure.get_structure())
        def creator(**kwargs):
            return Item(data=kwargs).save()

        creator.__name__ = "create_" + self.name

        return creator


    def get_getter(self):
        pass


class Item(Document):

    data = DictField()

    category = ReferenceField(Category)


human = Category.objects(pk="human").first()

if not human:
    weight = DBArg(name="weight", params={'max_val': 500, 'min_val':0, 'required': True}).save()
    height = DBArg(name="height", params={'max_val': 290}).save()
    human_argstructure = DBStruct(args=[weight, height]).save()
    human = Category(name="human", arg_structure=human_argstructure).save()

register_human = human.get_creator()