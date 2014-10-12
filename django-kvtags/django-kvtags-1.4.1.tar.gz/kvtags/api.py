from tastypie.resources import ModelResource
from tastypie.constants import ALL
from tastypie import fields
from kvtags.models import *


class TagResource(ModelResource):
    kv_pairs = fields.ToManyField('kvtags.api.KeyValueResource', 'kv_pairs', full=True)

    class Meta:
        queryset = Tag.objects.all()
        filtering = {
            "key": ALL
        }
        resource_name = 'tag'
        excludes = ['created', 'updated']
        include_resource_uri = False


class KeyValueResource(ModelResource):
    tag = fields.ForeignKey(TagResource, 'tag')

    class Meta:
        queryset = KeyValue.objects.all()
        filtering = {
            "tag": ALL,
            "key": ALL,
            "value": ALL
        }
        resource_name = 'tag-kv'
        include_resource_uri = False


class TaggedItemResource(ModelResource):
    tag = fields.ForeignKey(TagResource, 'tag')

    class Meta:
        queryset = TaggedItem.objects.all()
        resource_name = 'tagged-item'