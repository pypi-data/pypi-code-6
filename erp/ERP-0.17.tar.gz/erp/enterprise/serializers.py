__author__ = 'cltanuki'
from rest_framework import serializers

from .models import CorpUser, CorpUnit, CorpObject


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CorpUser
        fields = ('username',)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CorpUnit
        fields = '__all__'


class ObjSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CorpObject
        fields = '__all__'