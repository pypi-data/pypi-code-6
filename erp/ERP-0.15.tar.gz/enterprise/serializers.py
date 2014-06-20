__author__ = 'cltanuki'
from .models import CorpUser, CorpUnit, CorpObject
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CorpUser
        fields = ('username', 'email', 'corp_group', 'first_name', 'last_name', 'mid_name', 'date_of_birth', 'phone')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CorpUnit
        fields = '__all__'


class ObjSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CorpObject
        fields = '__all__'