from rest_framework import serializers
from rest_framework.reverse import reverse

from . import fields, mixins, models
from pages.utils import build_url


class PageSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField()
    regions = serializers.SerializerMethodField('rendered_regions')

    class Meta:
        fields = ('id', 'url', 'name', 'slug', 'regions')
        model = models.Page
        view_name = 'pages:page-detail'

    def rendered_regions(self, obj):
        return obj.rendered_regions(self.context['request'])


class GroupSerializer(mixins.LinksMixin, serializers.HyperlinkedModelSerializer):
    url = fields.AbsoluteURLIdentityField()
    pages = serializers.SerializerMethodField('get_pages_link')

    links_fields = ['pages']

    class Meta:
        model = models.Group

    def get_pages_link(self, obj):
        return build_url(
            reverse('pages:page-list', request=self.context.get('request')),
            {'group': obj.slug},
        )
