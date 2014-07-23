'''
Created on Jul 19, 2014

@author: Kenneth
'''
from addresses.models import Province, City
from rest_framework import serializers


class ProvinceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Province
        fields = ('url', 'name', 'island_group', 'country')


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ('url', 'name')
